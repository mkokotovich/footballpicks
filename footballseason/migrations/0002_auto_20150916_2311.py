# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('footballseason', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='loses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='ties',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
