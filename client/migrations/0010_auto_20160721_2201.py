# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_auto_20160721_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='client',
            name='facebook_form_id',
            field=models.CharField(max_length=120),
        ),
    ]
