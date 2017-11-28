# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 08:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0010_auto_20171108_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]