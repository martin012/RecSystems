# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_restaurant_restaurant_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='food',
            new_name='restaurant',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='tag',
            new_name='food',
        ),
    ]
