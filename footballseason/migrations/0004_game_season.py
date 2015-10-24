# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('footballseason', '0003_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.IntegerField(default=0),
        ),
    ]
