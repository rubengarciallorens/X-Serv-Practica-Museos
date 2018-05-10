# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identidad', models.TextField(default=b'DEFAULT_VALUE')),
                ('nombre', models.TextField(default=b'DEFAULT_VALUE')),
                ('descripcion_entidad', models.TextField(default=b'DEFAULT_VALUE')),
                ('equipamiento', models.TextField(default=b'DEFAULT_VALUE')),
                ('transporte', models.TextField(default=b'DEFAULT_VALUE')),
                ('descripcion', models.TextField(default=b'DEFAULT_VALUE')),
                ('horario', models.TextField(default=b'DEFAULT_VALUE')),
                ('accesibilidad', models.TextField(default=b'DEFAULT_VALUE')),
                ('url', models.TextField(default=b'DEFAULT_VALUE')),
                ('localizacion', models.TextField(default=b'DEFAULT_VALUE')),
                ('contacto', models.TextField(default=b'DEFAULT_VALUE')),
                ('tipo', models.TextField(default=b'DEFAULT_VALUE')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_text', models.TextField(default=b'DEFAULT_VALUE')),
            ],
        ),
    ]
