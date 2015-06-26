# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.main.models import (
    Application,
	ApplicationForm,
	ApplicationCase,
	Applicant,
    ApplicationComment,
    HandoveredDocument
)

# Register your models here.

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'application_case', 'applied_time', 'author')
    list_display_links = ('applicant', )
    search_fields = ['applicant__id_no', 'applicant__fullname']
    list_filter = ['application_case__name', 'author__first_name']


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'id_no', 'phone', 'registered_address')
    list_display_links = ('fullname', )
    search_fields = ['id_no', 'fullname', 'phone', 'registered_address']

@admin.register(ApplicationCase)
class ApplicationCaseAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'scan_file')

@admin.register(ApplicationComment)
class ApplicationCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(HandoveredDocument)
class HandoveredDocumentAdmin(admin.ModelAdmin):
    pass
