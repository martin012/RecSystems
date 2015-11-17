# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('food_name', models.CharField(max_length=50)),
                ('food_photo', models.ImageField(upload_to='images/food/')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('restaurant_name', models.CharField(max_length=50)),
                ('restaurant_description', models.CharField(max_length=50)),
                ('restaurant_photo', models.ImageField(upload_to='images/restaurant/')),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='food',
            field=models.ForeignKey(to='food.Restaurant'),
        ),
    ]
