# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newlead',
            name='form_id',
            field=models.CharField(default='', max_length=120),
        ),
    ]
