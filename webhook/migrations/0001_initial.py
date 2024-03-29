# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewLead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.CharField(max_length=120)),
                ('form_id', models.CharField(default=None, max_length=120)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
