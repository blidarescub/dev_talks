# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike_api', '0003_auto_20151121_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='uid',
            field=models.CharField(default='adRYJoF8ivUcrsJcm4LWxX4vaXYTpXQuyveVjPTJjtlSAoosxqMeg4vBEAZ1VuGR', max_length=64),
        ),
    ]
