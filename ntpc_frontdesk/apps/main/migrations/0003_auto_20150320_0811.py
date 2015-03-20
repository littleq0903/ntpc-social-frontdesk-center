# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20150318_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='involved_servers',
            field=models.ManyToManyField(related_name='involved_servers', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='server',
            field=models.ForeignKey(related_name='main_server', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
