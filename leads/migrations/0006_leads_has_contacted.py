# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 05:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0005_remove_leads_has_contacted'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='has_contacted',
            field=models.BooleanField(default=False),
        ),
    ]
