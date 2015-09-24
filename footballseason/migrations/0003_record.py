# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('footballseason', '0002_auto_20150916_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('user_name', models.CharField(max_length=200)),
                ('season', models.IntegerField(default=0)),
                ('week', models.IntegerField(default=0)),
                ('wins', models.IntegerField(default=0)),
            ],
        ),
    ]
