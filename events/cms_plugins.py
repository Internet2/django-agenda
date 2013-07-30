from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import operator
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from plaza2.apps.bloat.library import get_page_tags

from taggit.models import Tag

from events.models import Event, Calendar, EventsPluginModel

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
        now = datetime.now()      

        #print "Events: %s" % events

        if instance.date_start_today:
            events = events.filter(event_date__gte = now)
        elif instance.date_start:
            events = events.filter(event_date__gte = instance.date_start)

        #print "Events (post-start date): %s" % events

        if instance.date_end_yesterday:
           events = events.filter(end_date__lte=now - timedelta(days=1))
        elif instance.date_end:
            events = events.filter(end_date__lte = instance.date_end)

        #print "Events (post-end date): %s" % events

        # Default
        if not instance.date_start_today and not instance.date_end_yesterday and instance.date_start == None and instance.date_end == None:
            events = events.filter(end_date__gte=now - timedelta(days=1))

        #print "Events (post-default dates): %s" % events

        if instance.display_date_as == "descending":
            events = events.order_by("-event_date")
        else:
            events = events.order_by("event_date")

        #print "Events (ordering): %s" % events

        tag_filters = []

        if instance.use_page_tags:
            #print "Using Page Tags: %s" % get_page_tags(instance.page)
            tag_filters.extend(get_page_tags(instance.page))

        tag_filters.extend(instance.tags.all())

        if len(tag_filters) > 0:
            #print "Events (tag filters): %s" % tag_filters

            events = events.filter(tags__in = tag_filters).distinct()
 
        #print "Events (post-tag filters): %s" % events

        if instance.calendars.count() > 0:
            calendar_filters = []
            for calendar in instance.calendars.all():
                calendar_filters.append(Q(calendar = calendar))
            events = events.filter(reduce(operator.or_, calendar_filters))

        #print "Events (post-calendars): %s" % events

        context['more'] = instance.more
        context['events_list'] = events[:instance.limit]
        context['display_as'] = instance.display_as
        #self.render_template = instance.display
        return context


plugin_pool.register_plugin(EventsPlugin)
