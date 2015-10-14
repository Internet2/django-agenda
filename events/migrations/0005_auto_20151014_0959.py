# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager
import datetime
import django.contrib.sites.managers
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150820_1317'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='event',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
                ('published', events.models.PublicationManager()),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 9, 59, 45, 260088), verbose_name='publication date'),
        ),
    ]
