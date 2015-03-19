# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationcase',
            name='notes',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
