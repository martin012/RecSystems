# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='food_rating',
            field=models.DecimalField(max_digits=2, default=0.0, decimal_places=1),
        ),
    ]
