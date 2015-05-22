# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150405_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='HandoveredDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scan_file', models.FileField(null=True, upload_to=b'', blank=True)),
                ('case', models.ForeignKey(to='main.ApplicationForm')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='application',
            name='author',
            field=models.ForeignKey(related_name='applications', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='handovered_forms',
            field=models.ManyToManyField(related_name='related_application', null=True, to='main.HandoveredDocument', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='involved_authors',
            field=models.ManyToManyField(related_name='involved_applications', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
