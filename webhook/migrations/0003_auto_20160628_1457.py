# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0002_auto_20160628_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newlead',
            name='form_id',
            field=models.CharField(max_length=120),
        ),
    ]
