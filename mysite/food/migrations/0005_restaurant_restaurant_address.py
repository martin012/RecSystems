# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_auto_20151204_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='restaurant_address',
            field=models.CharField(default='', max_length=50),
        ),
    ]
