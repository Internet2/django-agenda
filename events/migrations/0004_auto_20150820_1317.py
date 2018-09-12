# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150310_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 20, 13, 17, 18, 804816), verbose_name='publication date'),
            preserve_default=True,
        ),
    ]
