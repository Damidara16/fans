# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-16 00:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20181010_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preview',
            name='content',
        ),
        migrations.RemoveField(
            model_name='preview',
            name='user',
        ),
        migrations.DeleteModel(
            name='Preview',
        ),
    ]
