# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0005_auto_20180518_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='comentario',
        ),
        migrations.AddField(
            model_name='comentario',
            name='texto',
            field=models.TextField(default='DEFAULT_VALUE'),
        ),
    ]
