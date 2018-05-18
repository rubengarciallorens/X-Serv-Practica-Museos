# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0008_museo_añadido'),
    ]

    operations = [
        migrations.AddField(
            model_name='seleccion',
            name='nombre',
            field=models.TextField(default='DEFAULT_VALUE'),
        ),
        migrations.AlterField(
            model_name='seleccion',
            name='museos_fav',
            field=models.ManyToManyField(to='museos.Museo_añadido'),
        ),
    ]
