from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models import Q
import operator
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from plaza2.apps.bloat.library import limit_object_list, build_tags_list, get_page_tags

from taggit.models import Tag

from events.models import Event, Calendar, EventsPluginModel

from library import query_events, output_date_range

class EventsPluginForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        Tag.objects.all().order_by("name"),
        widget=FilteredSelectMultiple("tags", False),
        required=False)
    calendars = forms.ModelMultipleChoiceField(
        Calendar.objects.all().order_by("name"),
        widget=FilteredSelectMultiple("calendars", False),
        required=False)

    class Meta:
        model = EventsPluginModel
 
class EventsPlugin(CMSPluginBase):
    model = EventsPluginModel
    name = _("Events")
    render_template = "events_plugin.html"
    form = EventsPluginForm
 
    def render(self, context, instance, placeholder):
        events = Event.objects.all()

        #print "Events: %s" % events

        min_start_date = None
        max_start_date = None
        min_end_date   = None
        max_end_date   = None

        if instance.date_start_today:
            min_start_date = timezone.now()
        elif instance.date_start:
            min_start_date = instance.date_start

        if instance.date_end_yesterday:
            max_end_date = timezone.now() - timedelta(days=1)
        elif instance.date_end:
            max_end_date = instance.date_end

        # Default
        if not instance.date_start_today and not instance.date_end_yesterday and instance.date_start == None and instance.date_end == None:
            min_end_date = timezone.now() - timedelta(days=1)

        tags = []
        if instance.use_page_tags:
            tags.extend(map(lambda x: x.slug, get_page_tags(instance.page)))
        tags.extend(map(lambda x: x.slug, instance.tags.all()))

        calendars = map(lambda x: x.slug, instance.calendars.all())

        events = query_events(calendars=calendars, tags=tags, ordering=instance.display_date_as,
                          min_start_date=min_start_date, max_start_date=max_start_date,
                          min_end_date=min_end_date, max_end_date=max_end_date)
 
        #print "Events (post-calendars): %s" % events

        events, has_more = limit_object_list(events, limit=instance.limit)

        context['events_list'] = events
        if instance.more:
            context['more'] = has_more
        context['display_as'] = instance.display_as
        context['tags_str'] = build_tags_list(map(lambda x: Tag.objects.get(slug=x), tags))
        context['calendars_str'] = build_tags_list(instance.calendars.all())
        context['ordering_str'] = instance.display_as
        context['start_date_str'] = output_date_range([ min_start_date, max_start_date ])
        context['end_date_str'] = output_date_range([ min_end_date, max_end_date ])
        #self.render_template = instance.display
        return context


plugin_pool.register_plugin(EventsPlugin)
