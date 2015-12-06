# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_auto_20151206_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='restaurant_address',
            field=models.CharField(max_length=100, default=''),
        ),
    ]
