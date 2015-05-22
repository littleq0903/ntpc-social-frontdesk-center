# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20150521_0600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='handovered_forms',
        ),
        migrations.AlterField(
            model_name='handovereddocument',
            name='application',
            field=models.ForeignKey(related_name='handovered_forms', to='main.ApplicationForm'),
            preserve_default=True,
        ),
    ]
