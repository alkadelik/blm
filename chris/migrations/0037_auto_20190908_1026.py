# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-08 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chris', '0036_bank_recipient_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='acc_no',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]