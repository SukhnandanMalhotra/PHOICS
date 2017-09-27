# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-24 05:16
from __future__ import unicode_literals

from django.db import migrations, models
import portal.models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to=portal.models.get_profile_name),
        ),
    ]
