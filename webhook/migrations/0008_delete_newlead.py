# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 15:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0007_newlead_ad_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewLead',
        ),
    ]