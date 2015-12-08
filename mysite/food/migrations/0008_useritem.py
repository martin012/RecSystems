# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food', '0007_auto_20151206_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=2)),
                ('food', models.ForeignKey(to='food.Food')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
