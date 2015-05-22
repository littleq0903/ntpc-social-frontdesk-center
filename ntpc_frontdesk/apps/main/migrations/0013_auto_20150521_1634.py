# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20150521_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='handovereddocument',
            name='form_type',
            field=models.ForeignKey(related_name='+', default=2, to='main.ApplicationForm'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='handovereddocument',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 21, 16, 34, 9, 656131, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
