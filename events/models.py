from datetime import datetime
from django.utils import timezone

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.conf import settings

from django.contrib.auth.models import User

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from django.contrib.sitemaps import ping_google

from cms.models.pluginmodel import CMSPlugin

from taggit.models import Tag
 

class PublicationManager(CurrentSiteManager):
    def get_query_set(self):
        return super(CurrentSiteManager, self).get_query_set().filter(publish=True, publish_date__lte=timezone.now())

class Event(models.Model):
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['-event_date', '-end_date', '-start_time', '-title']
        get_latest_by = 'event_date'
        permissions = (("change_author", ugettext("Change author")),)
        unique_together = ("event_date", "slug")

    def __unicode__(self):
        return _("%(title)s on %(event_date)s") % { 'title'      : self.title,
                                                    'event_date' : self.event_date }

    @models.permalink                                               
    def get_absolute_url(self):
        return ('agenda-detail', (), {
                  'year'  : self.event_date.year, 
                  'month' : self.event_date.month, 
                  'day'   : self.event_date.day, 
                  'slug'  : self.slug })
        
    objects = models.Manager()
    on_site = CurrentSiteManager()
    published = PublicationManager()

    # Core fields
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), db_index=True)
    
    event_date = models.DateField(_('date'), help_text="Enter single date here, or event start date")
    
    #event_date can double as start_date 
    end_date = models.DateField(_('end date'), blank=True, null=True, help_text="Enter end date, can be blank.")
    
    start_time = models.TimeField(_('start time'), blank=True, null=True)
    end_time = models.TimeField(_('end time'), blank=True, null=True)
    
    event_url = models.URLField(_('URL'), blank=True) #, verify_exists=True)
    
    location = models.CharField(_('location'), max_length=255)

    description = models.TextField(_('description'), blank=True)

    calendar = models.ForeignKey("Calendar", blank=True, null=True, related_name='events')

    submitter = models.CharField(_('submitter'), max_length=255, blank=True)

    time_zone = models.CharField(_('time_zone'), max_length=255, blank=True)

    old_events_id = models.IntegerField(_('old_events_id'), unique=True, null=True, blank=True, help_text="The identifier from the old events database")

    # Extra fields
    add_date = models.DateTimeField(_('add date'),auto_now_add=True)
    mod_date = models.DateTimeField(_('modification date'), auto_now=True)
    
    author = models.ForeignKey(User, verbose_name=_('author'), db_index=True, blank=True, null=True)

    publish_date = models.DateTimeField(_('publication date'), default=timezone.now())
    publish = models.BooleanField(_('publish'), default=True)
    
    allow_comments = models.BooleanField(_('Allow comments'), default=True)

    sites = models.ManyToManyField(Site)
    
    tags = models.ManyToManyField(Tag, blank=True)
    
    def save(self):
        if self.end_date is None:
            self.end_date = self.event_date
        super(Event, self).save()
        if not settings.DEBUG:
            try:
                ping_google()
            except Exception:
                import logging
                logging.warn('Google ping on save did not work.')

class Calendar(models.Model):
    name = models.CharField(_('name'), max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('calendar')
        verbose_name_plural = _('calendars')

    def __unicode__(self):
        if self.name:
            return self.name
        return _("Unnamed Calendar")

class EventsPluginModel(CMSPlugin):
    use_page_tags = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    calendars = models.ManyToManyField(Calendar, null=True, blank=True)
    EVENT_PLUGIN_DISPLAY_CHOICES = (
       ('list', 'List'),
       ('calendar', 'Calendar'),
       ('upcoming', 'Upcoming events div')
    )

    EVENT_PLUGIN_DATE_DISPLAY_CHOICES = (
        ('descending', 'Descending'),
        ('ascending', 'Ascending')
    )

    date_start_today = models.BooleanField(blank=True, default=False, help_text="Show events starting today?")
    date_start = models.DateTimeField("Start date", blank=True, null=True)
    date_end_yesterday = models.BooleanField(blank=True, default=False, help_text="Show events ending yesterday?")
    date_end = models.DateTimeField("End date", blank=True, null=True)
    display_date_as = models.CharField(max_length=20, choices=EVENT_PLUGIN_DATE_DISPLAY_CHOICES, default=EVENT_PLUGIN_DATE_DISPLAY_CHOICES[0][0]) 

    display_as = models.CharField(max_length=20, choices=EVENT_PLUGIN_DISPLAY_CHOICES, default=EVENT_PLUGIN_DISPLAY_CHOICES[0][0])
    limit = models.IntegerField(default=10)
    more = models.BooleanField(blank=True, default=True, help_text="Show more button?")
    
    def __unicode__(self):
        return u'%s' % (self.tags)

    def copy_relations(self, oldinstance):
        self.calendars = oldinstance.calendars.all()
