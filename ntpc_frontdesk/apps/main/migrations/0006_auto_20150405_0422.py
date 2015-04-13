# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150402_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationcomment',
            name='author',
            field=models.ForeignKey(related_name='committed_comments', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
