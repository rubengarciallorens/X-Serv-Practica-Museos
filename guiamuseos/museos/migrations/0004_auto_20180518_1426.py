# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0003_auto_20180518_1128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='museo',
            name='contacto',
        ),
        migrations.AddField(
            model_name='museo',
            name='email',
            field=models.TextField(default='DEFAULT_VALUE'),
        ),
        migrations.AddField(
            model_name='museo',
            name='fax',
            field=models.TextField(default='DEFAULT_VALUE'),
        ),
        migrations.AddField(
            model_name='museo',
            name='telefono',
            field=models.TextField(default='DEFAULT_VALUE'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='comentario',
            field=models.TextField(default='DEFAULT_VALUE'),
        ),
    ]
