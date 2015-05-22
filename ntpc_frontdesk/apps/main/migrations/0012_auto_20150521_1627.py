# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20150521_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='handovereddocument',
            name='application',
        ),
        migrations.AddField(
            model_name='application',
            name='handovered_forms',
            field=models.ManyToManyField(to='main.HandoveredDocument'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='handovereddocument',
            name='upload_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
