# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20161012_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_visit_dt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to='profile_image'),
        ),
    ]