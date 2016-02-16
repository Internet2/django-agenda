# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20151014_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 14, 6, 22, 931174), verbose_name='publication date'),
        ),
        migrations.AlterField(
            model_name='eventspluginmodel',
            name='calendars',
            field=models.ManyToManyField(to='events.Calendar', blank=True),
        ),
    ]
