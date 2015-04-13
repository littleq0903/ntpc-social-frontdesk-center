#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class ApplicationForm(models.Model):
    name = models.CharField(max_length=50)
    scan_file = models.FileField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class ApplicationCase(models.Model):
    name = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    required_forms = models.ManyToManyField(ApplicationForm, null=True, blank=True, related_name="case_required_this")

    def __unicode__(self):
        return self.name


class Applicant(models.Model):
    id_no = models.CharField(max_length=20)
    fullname = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s-%s" % (self.id_no, self.fullname)

    @property
    def gender(self):
        if self.id_no[1] == '1':
            return 'male'
        elif self.id_no[2] == '2':
            return 'female'
        else:
            return 'unknown'


class Application(models.Model):
    applicant = models.ForeignKey(Applicant)
    application_case = models.ForeignKey(ApplicationCase)
    applied_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name='applications')
    involved_authors = models.ManyToManyField(User, null=True, blank=True, related_name="involved_applications")
    handovered_forms = models.ManyToManyField(ApplicationForm, null=True, blank=True)
    
    def __unicode__(self):
        return u"%s: %s" % (self.application_case, self.applicant)


class ApplicationComment(models.Model):
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, related_name='committed_comments')
    target = models.ForeignKey(Application, related_name='comments')

    def __unicode__(self):
        return u"Comment: %s to %s" % (self.commenter, self.target)


