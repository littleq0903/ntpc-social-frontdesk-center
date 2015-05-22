# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20150521_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='living_address',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='applicant',
            name='phone',
            field=models.CharField(default='0226221020', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicant',
            name='registered_address',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
