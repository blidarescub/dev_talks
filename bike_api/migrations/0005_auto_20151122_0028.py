# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bike_api', '0004_users_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='zone',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='zone',
            name='longitude',
        ),
        migrations.AddField(
            model_name='location',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='zone',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='uid',
            field=models.CharField(default='oZKzQKWRvoINNPU7eWdl5gKDFEL6M55NusTc7JL1UjTqS24kLbrPSDDIMOYFdarN', max_length=64),
        ),
    ]
