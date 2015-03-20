# -*- coding: utf-8 -*-
"""
Serializers and ViewSets
"""
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response

from apps.main.models import ApplicationForm, ApplicationCase, Application, Applicant

# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()

# Users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'id', 'username', 'last_name', 'first_name', 'email')
        extra_kwargs = {
            'url': {'view_name': 'users', 'lookup_field': 'username'}
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
        fields = ('id_no', 'fullname')

# Application Form
class ApplicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = ('name', 'scan_file')

# Application Case
class ApplicationCaseSerializer(serializers.ModelSerializer):
    required_forms = serializers.SerializerMethodField()

    def get_required_forms(self, obj):
        # default serializer is not working in ManyToManyField, so we hacked one.
        if obj:
            return [ ApplicationFormSerializer(form).data for form in ApplicationForm.objects.filter(case_required_this=obj) ]

    class Meta:
        model = ApplicationCase
        fields = ('name', 'notes', 'required_forms')

# Application
class ApplicationSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer()
    application_case = ApplicationCaseSerializer()
    server = UserSerializer()

    class Meta:
        model = Application
        fields = (
            'applied_time',
            'modified_time',
            'id',
            'applicant',
            'application_case',
            'server',
            'involved_servers'
        )


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

ROUTER.register(r'applications', ApplicationViewSet)

