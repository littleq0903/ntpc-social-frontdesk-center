# -*- coding: utf-8 -*-
"""
Serializers and ViewSets
"""
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

import json

from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from apps.main.models import (
    ApplicationForm,
    HandoveredDocument,
    ApplicationCase,
    Application,
    Applicant,
    ApplicationComment
)

# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()


# Users
class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    def get_fullname(self, obj):
        fullname = obj.get_full_name()
        return fullname or obj.username

    class Meta:
        model = User
        fields = ('pk', 'id', 'username', 'last_name',
                  'first_name', 'email', 'fullname')
        extra_kwargs = {
            'url': {
                'view_name': 'users',
                'lookup_field': 'username'
            }
        }


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def retrieve(self, request, username=None):
        queryset = User.objects.all()

        if username == 'me':
            user = request.user
        else:
            user = get_object_or_404(queryset, username=username)

        serializer = UserSerializer(user)
        return Response(serializer.data)


ROUTER.register(r'users', UserViewSet)


# Applicant
class ApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant
        fields = ('id_no', 'fullname', 'gender', 'phone', 'registered_address', 'living_address')

class HandoveredDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandoveredDocument
        fields = ('scan_file', 'id', 'updated_time', 'form_type')

# Application Form
class ApplicationFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationForm
        fields = ('id', 'name', 'scan_file')


# Application Case
class ApplicationCaseSerializer(serializers.ModelSerializer):
    required_forms = serializers.SerializerMethodField()

    def get_required_forms(self, obj):
        # default serializer is not working in ManyToManyField, so we hacked one.
        if obj:
            return [ ApplicationFormSerializer(form).data for form in ApplicationForm.objects.filter(case_required_this=obj) ]

    class Meta:
        model = ApplicationCase
        fields = ('id', 'name', 'notes', 'required_forms')


class ApplicationCaseViewSet(viewsets.ModelViewSet):
    queryset = ApplicationCase.objects.all()
    serializer_class = ApplicationCaseSerializer

ROUTER.register(r'applicationcase', ApplicationCaseViewSet)


# Application
class ApplicationCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)

    class Meta:
        model = ApplicationComment
        fields = (
            'content',
            'created_time',
            'modified_time',
            'author',
            'target'
        )

def validator_list_of_ints(target):
    if not isinstance(target, list):
        raise serializers.ValidationError('Not a list')
    if filter(lambda x: not isinstance(x, int), target):
        raise serializers.ValidationError('All elements in this list should be intergers')

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer()
    application_case = ApplicationCaseSerializer()
    author = UserSerializer(required=False)
    comments = serializers.SerializerMethodField()
    handovered_forms = HandoveredDocumentSerializer(many=True)


    def get_comments(self, obj):
        if obj:
            return [ ApplicationCommentSerializer(cmt).data for cmt in ApplicationComment.objects.filter(target=obj) ]


    class Meta:
        model = Application
        fields = (
            'applied_time',
            'modified_time',
            'id',
            'applicant',
            'application_case',
            'author',
            'involved_authors',
            'comments',
            'notes',
            'handovered_forms'
        )
        depth = 1


class ApplicationSaveSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer()
    application_case = serializers.PrimaryKeyRelatedField(queryset=ApplicationCase.objects.all())
    handovered_forms_string = serializers.CharField()
    author_username = serializers.CharField()
    
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'application_case': ApplicationCaseSerializer().to_representation(obj.application_case),
            'applicant': ApplicantSerializer().to_representation(obj.applicant),
            'author': UserSerializer().to_representation(obj.author),
        }

    def create(self, validated_data):
    
        handovered_forms = json.loads(validated_data.pop('handovered_forms_string'))
        applicant_data = validated_data.pop('applicant')
        author_username = validated_data.pop('author_username')

        author = User.objects.get(username=author_username)

        applicant, applicant_existance = Applicant.objects.get_or_create(id_no=applicant_data['id_no'], defaults=applicant_data)
        applicant.save()

        validated_data['applicant'] = applicant
        validated_data['author'] = author

        
        app = Application.objects.create(**validated_data)
        app.save()

        for form in handovered_forms:
            targetform = ApplicationForm.objects.get(pk=form)
            document = HandoveredDocument.objects.create(form_type=targetform)
            document.save()

            app.handovered_forms.add(document)
            
        app.save()

        return app

    def update(self, instance, validated_data):
        handovered_forms = json.loads(validated_data.pop('handovered_forms_string'))
        existed_forms = map(lambda x: x.form_type.id, instance.handovered_forms.all())

        forms_toadd = set(handovered_forms) - set(existed_forms)
        forms_todelete = set(existed_forms) - set(handovered_forms)

        instance.notes = validated_data['notes']

        for form in forms_toadd:
            targetform = ApplicationForm.objects.get(id=form)
            document = HandoveredDocument.objects.create(form_type=targetform)
            document.save()

            instance.handovered_forms.add(document)

        for form in forms_todelete:
            targetform = ApplicationForm.objects.get(id=form)
            document = instance.handovered_forms.filter(form_type=targetform)
            document.delete()

        instance.save()

        return instance

    class Meta:
        model = Application
        fields = (
            'applicant',
            'application_case',
            'handovered_forms_string',
            'author_username',
            'notes'
        )

    
class MultiSerializerModelViewSet(viewsets.ModelViewSet):
    serializers = {
        'default': None
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


class ApplicationViewSet(MultiSerializerModelViewSet):
    queryset = Application.objects.all().order_by("-modified_time")
    serializers = {
        'default': ApplicationSerializer,
        'list': ApplicationSerializer,
        'get': ApplicationSerializer,
        'update': ApplicationSaveSerializer,
        'create': ApplicationSaveSerializer
    }


class ApplicationCommentViewSet(viewsets.ModelViewSet):
    queryset = ApplicationComment.objects.all()
    serializer_class = ApplicationCommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        

ROUTER.register(r'applications', ApplicationViewSet)
ROUTER.register(r'comments', ApplicationCommentViewSet)

