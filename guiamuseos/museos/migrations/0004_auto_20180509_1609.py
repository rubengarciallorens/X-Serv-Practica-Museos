# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0003_museo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='museo',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='museo',
            name='url',
        ),
    ]
