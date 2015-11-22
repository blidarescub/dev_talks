# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bikes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('free', models.BooleanField(default=True)),
                ('damaged', models.BooleanField(default=False)),
                ('distance', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'bikes',
                'verbose_name_plural': 'bikes',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'location',
                'verbose_name_plural': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=255)),
                ('distance', models.IntegerField(default=0)),
                ('bike', models.ForeignKey(to='bike_api.Bikes')),
                ('location', models.ForeignKey(to='bike_api.Location')),
            ],
            options={
                'db_table': 'users',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'zones',
                'verbose_name_plural': 'zones',
            },
        ),
        migrations.AddField(
            model_name='location',
            name='zone',
            field=models.ForeignKey(to='bike_api.Zone'),
        ),
        migrations.AddField(
            model_name='bikes',
            name='location',
            field=models.ForeignKey(to='bike_api.Location'),
        ),
    ]
