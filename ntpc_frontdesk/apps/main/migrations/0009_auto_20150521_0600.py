# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_application_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='handovereddocument',
            old_name='case',
            new_name='application',
        ),
    ]
