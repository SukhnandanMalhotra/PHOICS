# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 07:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_document_reset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='reset',
        ),
    ]
