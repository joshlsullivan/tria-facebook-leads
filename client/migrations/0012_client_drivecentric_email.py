# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_client_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='drivecentric_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
