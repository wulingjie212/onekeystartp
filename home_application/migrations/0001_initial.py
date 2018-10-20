# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_id', models.IntegerField()),
                ('bussiness', models.CharField(max_length=50)),
                ('ip', models.CharField(max_length=20)),
                ('creator', models.CharField(max_length=10)),
                ('config_dsc', models.TextField()),
                ('cpu_monitor', models.TextField()),
            ],
        ),
    ]
