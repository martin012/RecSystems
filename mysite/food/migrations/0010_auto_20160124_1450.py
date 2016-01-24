# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_rating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.AlterField(
            model_name='food',
            name='food_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='useritem',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
