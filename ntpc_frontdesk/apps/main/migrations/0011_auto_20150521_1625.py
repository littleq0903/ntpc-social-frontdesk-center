# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20150521_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handovereddocument',
            name='application',
            field=models.ForeignKey(to='main.ApplicationForm'),
            preserve_default=True,
        ),
    ]
