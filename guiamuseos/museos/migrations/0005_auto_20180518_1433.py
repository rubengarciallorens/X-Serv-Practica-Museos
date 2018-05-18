# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0004_auto_20180518_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museo',
            name='email',
            field=models.TextField(default='No proporcionado'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='fax',
            field=models.TextField(default='No proporcionado'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='tipo',
            field=models.TextField(default='No proporcionado'),
        ),
    ]
