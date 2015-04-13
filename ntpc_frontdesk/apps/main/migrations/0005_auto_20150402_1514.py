# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_auto_20150323_0759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='server',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='involved_servers',
            new_name='involved_authors',
        ),
        migrations.RemoveField(
            model_name='applicationcomment',
            name='commenter',
        ),
        migrations.AddField(
            model_name='applicationcomment',
            name='author',
            field=models.ForeignKey(related_name='committed_comments', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
