# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150310_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 10, 15, 12, 16, 92936), verbose_name='publication date'),
            preserve_default=True,
        ),
    ]
