# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0007_museo_num_comentarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Museo_añadido',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('añadido', models.DateTimeField(default=django.utils.timezone.now)),
                ('museo', models.ForeignKey(to='museos.Museo')),
            ],
        ),
    ]
