# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0006_auto_20180518_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='num_comentarios',
            field=models.IntegerField(default=0),
        ),
    ]
