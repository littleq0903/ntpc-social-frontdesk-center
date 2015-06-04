#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class ApplicationForm(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"名稱")
    scan_file = models.FileField(null=True, blank=True, verbose_name=u"申請表檔案", upload_to="appform_files")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'應備文件'
        verbose_name_plural = u'應備文件'

class HandoveredDocument(models.Model):
    form_type = models.ForeignKey(ApplicationForm, related_name='+')
    scan_file = models.FileField(null=True, blank=True)
    upload_time = models.DateTimeField(null=True, blank=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'繳交文件: %s' % self.form_type.name

    class Meta:
        verbose_name = u'已繳交文件'
        verbose_name_plural = u'已繳交文件'


class ApplicationCase(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"業務名稱")
    notes = models.TextField(blank=True, verbose_name=u"注意事項")
    required_forms = models.ManyToManyField(ApplicationForm, null=True, blank=True, related_name="case_required_this", verbose_name=u"應備文件")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'承辦業務'
        verbose_name_plural = u'承辦業務'


class Applicant(models.Model):
    id_no = models.CharField(max_length=20, verbose_name=u"身份證字號")
    fullname = models.CharField(max_length=20, verbose_name=u"全名")
    phone = models.CharField(max_length=30, verbose_name=u"聯絡電話")
    registered_address = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"戶籍地址")
    living_address = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"通訊地址")

    def __unicode__(self):
        return u"%s-%s" % (self.id_no, self.fullname)

    def delete(self):
        # perform deleting all related applications
        # p.s. and the applications will delete all related documents automatically
        Application.objects.filter(applicant=self).delete()
        return super(Applicant, self).delete()

    @property
    def gender(self):
        if self.id_no[1] == '1':
            return 'male'
        elif self.id_no[2] == '2':
            return 'female'
        else:
            return 'unknown'

    class Meta:
        verbose_name = u'申請人'
        verbose_name_plural = u'申請人'


class Application(models.Model):
    applicant = models.ForeignKey(Applicant, verbose_name=u"申請人")
    application_case = models.ForeignKey(ApplicationCase, verbose_name=u"案件類別")
    applied_time = models.DateTimeField(auto_now_add=True, verbose_name=u"申請時間")
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u"上次修改時間")
    author = models.ForeignKey(User, related_name='applications', verbose_name=u"承辦人")
    involved_authors = models.ManyToManyField(User, null=True, blank=True, related_name="involved_applications", verbose_name=u"經手人員")
    notes = models.TextField(null=True, blank=True, verbose_name=u"案件備註")
    handovered_forms = models.ManyToManyField(HandoveredDocument, verbose_name=u"已繳交文件")

    def delete(self):
        # perform deleting all related commments
        ApplicationComment.objects.filter(target=self).delete()

        # perform deleting all related handovered documents
        self.handovered_forms.all().delete()
        return super(Application, self).delete()
    
    def __unicode__(self):
        return u"案件：%s" % (self.applicant)

    class Meta:
        verbose_name = u'已申請案件'
        verbose_name_plural = u'已申請案件'


class ApplicationComment(models.Model):
    content = models.TextField(verbose_name=u"內容")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u"留言時間")
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u"修改時間")
    author = models.ForeignKey(User, null=True, related_name='committed_comments', verbose_name=u"留言者")
    target = models.ForeignKey(Application, related_name='comments', verbose_name=u"留言案件")

    def __unicode__(self):
        return u"Comment: %s to %s" % (self.author, self.target.id)


    class Meta:
        verbose_name = u'案件留言'
        verbose_name_plural = u'案件留言'

