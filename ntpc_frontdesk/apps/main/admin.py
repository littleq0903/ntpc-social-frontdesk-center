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
    pass

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    pass

@admin.register(ApplicationCase)
class ApplicationCaseAdmin(admin.ModelAdmin):
    pass

@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    pass

@admin.register(ApplicationComment)
class ApplicationCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(HandoveredDocument)
class HandoveredDocumentAdmin(admin.ModelAdmin):
    pass
