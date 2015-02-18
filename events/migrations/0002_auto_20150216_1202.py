# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 16, 12, 2, 45, 169343), verbose_name='publication date'),
            preserve_default=True,
        ),
    ]
