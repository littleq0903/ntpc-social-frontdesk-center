#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from sequence_field.fields import SequenceField

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


class ApplicationSequence(models.Model):
    last_issued_date = models.DateField(auto_now=True)
    last_issued_number = models.IntegerField(default=1)

    @classmethod
    def get_or_create_if_missing(cls):
        if ApplicationSequence.objects.count() == 1:
            return ApplicationSequence.objects.all()[0]
        else:
            # missing, so create.
            app_seq = ApplicationSequence.objects.create()
            app_seq.save()
            return app_seq
            
    @classmethod
    def issue_number(cls):
        import datetime
        today = datetime.date.today()

        app_seq = cls.get_or_create_if_missing()

        if today == app_seq.last_issued_date:
            # the same date, increase the number by 1
            app_seq.last_issued_number += 1
            app_seq.save()
        else:
            # the different date, set the number to 1
            app_seq.last_issued_number = 1
            app_seq.save()
            # the last_issued_date will be automatically set by auto_now

        return (app_seq.last_issued_number, app_seq.last_issued_date)

    @classmethod
    def issue_formatted_number(cls, taiwan_format=True):
        year_delta = 1911 if taiwan_format else 0

        issued_num, issued_date = cls.issue_number()
        issued_date = (issued_date.year - year_delta, issued_date.month, issued_date.day)
        
        return int("%03d%02d%02d%04d" % (issued_date[0], issued_date[1], issued_date[2], issued_num))


class Application(models.Model):
    applicant = models.ForeignKey(Applicant, verbose_name=u"申請人")
    application_case = models.ForeignKey(ApplicationCase, verbose_name=u"案件類別")
    applied_time = models.DateTimeField(auto_now_add=True, verbose_name=u"申請時間")
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u"上次修改時間")
    author = models.ForeignKey(User, related_name='applications', verbose_name=u"承辦人")
    involved_authors = models.ManyToManyField(User, null=True, blank=True, related_name="involved_applications", verbose_name=u"經手人員")
    notes = models.TextField(null=True, blank=True, verbose_name=u"案件備註")
    handovered_forms = models.ManyToManyField(HandoveredDocument, verbose_name=u"已繳交文件")
    serial_number = models.IntegerField(verbose_name=u"案號")

    def save(self, *args, **kwargs):
        if not self.serial_number:
            self.serial_number = ApplicationSequence.issue_formatted_number()

        super(Application, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # perform deleting all related commments
        ApplicationComment.objects.filter(target=self).delete()

        # perform deleting all related handovered documents
        self.handovered_forms.all().delete()
        return super(Application, self).delete(*args, **kwargs)
    
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

