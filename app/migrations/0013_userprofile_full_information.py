# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20161012_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='full_information',
            field=models.BooleanField(default=False),
        ),
    ]