# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_remove_document_rotate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='height',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='document',
            name='width',
            field=models.IntegerField(),
        ),
    ]