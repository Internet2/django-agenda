# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20150310_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='name', blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'calendar',
                'verbose_name_plural': 'calendars',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('event_date', models.DateField(help_text=b'Enter single date here, or event start date', verbose_name='date')),
                ('end_date', models.DateField(help_text=b'Enter end date, can be blank.', null=True, verbose_name='end date', blank=True)),
                ('start_time', models.TimeField(null=True, verbose_name='start time', blank=True)),
                ('end_time', models.TimeField(null=True, verbose_name='end time', blank=True)),
                ('event_url', models.URLField(verbose_name='URL', blank=True)),
                ('location', models.CharField(max_length=255, verbose_name='location')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('submitter', models.CharField(max_length=255, verbose_name='submitter', blank=True)),
                ('time_zone', models.CharField(max_length=255, verbose_name='time_zone', blank=True)),
                ('old_events_id', models.IntegerField(help_text=b'The identifier from the old events database', unique=True, null=True, verbose_name='old_events_id', blank=True)),
                ('add_date', models.DateTimeField(verbose_name='add date', editable=False, blank=True)),
                ('mod_date', models.DateTimeField(verbose_name='modification date', editable=False, blank=True)),
                ('publish_date', models.DateTimeField(default=datetime.datetime(2015, 3, 10, 15, 11, 43, 439335), verbose_name='publication date')),
                ('publish', models.BooleanField(default=True, verbose_name='publish')),
                ('allow_comments', models.BooleanField(default=True, verbose_name='Allow comments')),
            ],
            options={
                'get_latest_by': 'event_date',
                'ordering': ['-event_date', '-end_date', '-start_time', '-title'],
                'verbose_name_plural': 'events',
                'verbose_name': 'event',
                'permissions': (('change_author', 'Change author'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventsPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin', on_delete=models.CASCADE)),
                ('use_page_tags', models.BooleanField(default=False)),
                ('date_start_today', models.BooleanField(default=False, help_text=b"Show current and future events as of 'today'?")),
                ('date_start', models.DateTimeField(null=True, verbose_name=b'Start date', blank=True)),
                ('date_end_yesterday', models.BooleanField(default=False, help_text=b"Show events that are over as of 'today'?")),
                ('date_end', models.DateTimeField(null=True, verbose_name=b'End date', blank=True)),
                ('display_date_as', models.CharField(default=b'descending', max_length=20, choices=[(b'descending', b'Descending'), (b'ascending', b'Ascending')])),
                ('display_as', models.CharField(default=b'list', max_length=20, choices=[(b'list', b'List'), (b'calendar', b'Calendar'), (b'upcoming', b'Upcoming events div')])),
                ('limit', models.IntegerField(default=10)),
                ('more', models.BooleanField(default=True, help_text=b'Show more button?')),
                ('calendars', models.ManyToManyField(to='events.Calendar', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
