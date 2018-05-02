# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(default=0)),
                ('game_time', models.DateTimeField(verbose_name='Game time')),
            ],
        ),
        migrations.CreateModel(
            name='Pick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('date_submitted', models.DateTimeField(verbose_name='Date pick was submitted')),
                ('game', models.ForeignKey(to='footballseason.Game', on_delete=models.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='pick',
            name='team_to_win',
            field=models.ForeignKey(to='footballseason.Team', on_delete=models.PROTECT),
        ),
        migrations.AddField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(related_name='game_away_team', to='footballseason.Team', on_delete=models.PROTECT),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(related_name='game_home_team', to='footballseason.Team', on_delete=models.PROTECT),
        ),
    ]
