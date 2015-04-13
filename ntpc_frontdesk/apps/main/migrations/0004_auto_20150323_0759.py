# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20150320_0811'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('commenter', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(related_name='comments', to='main.Application')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='application',
            name='handovered_forms',
            field=models.ManyToManyField(to='main.ApplicationForm', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='involved_servers',
            field=models.ManyToManyField(related_name='application_involved', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='applicationcase',
            name='required_forms',
            field=models.ManyToManyField(related_name='case_required_this', null=True, to='main.ApplicationForm', blank=True),
            preserve_default=True,
        ),
    ]
