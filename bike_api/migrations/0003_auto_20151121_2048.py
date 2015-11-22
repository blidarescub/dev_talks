# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike_api', '0002_remove_location_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikes',
            name='location',
            field=models.ForeignKey(blank=True, to='bike_api.Location', null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='bike',
            field=models.ForeignKey(blank=True, to='bike_api.Bikes', null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='location',
            field=models.ForeignKey(blank=True, to='bike_api.Location', null=True),
        ),
    ]
