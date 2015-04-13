# -*- coding: utf-8 -*-
"""
Serializers and ViewSets
"""
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from apps.main.models import (
    ApplicationForm,
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
        fields = ('id_no', 'fullname', 'gender')


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


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer()
    application_case = ApplicationCaseSerializer()
    author = UserSerializer()
    comments = serializers.SerializerMethodField()

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
            'comments'
        )


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationCommentViewSet(viewsets.ModelViewSet):
    queryset = ApplicationComment.objects.all()
    serializer_class = ApplicationCommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        

ROUTER.register(r'applications', ApplicationViewSet)
ROUTER.register(r'comments', ApplicationCommentViewSet)

