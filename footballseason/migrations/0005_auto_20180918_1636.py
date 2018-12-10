# Generated by Django 2.0.5 on 2018-09-18 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('footballseason', '0004_game_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pick',
            name='date_submitted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date pick was submitted'),
        ),
        migrations.AlterField(
            model_name='pick',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='picks', to='footballseason.Game'),
        ),
    ]
