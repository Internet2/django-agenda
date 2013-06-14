from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import operator

from events.models import Event, Calendar, EventsPluginModel

class EventsPlugin(CMSPluginBase):
    model = EventsPluginModel
    name = _("Events")
    render_template = "events_plugin.html"
    
    def render(self, context, instance, placeholder):
        events = Event.objects.all()
        now = datetime.now()      

        if instance.date_start_today:
            events = events.filter(event_date__gte = now)
        elif instance.date_start:
            events = events.filter(event_date__gte = instance.date_start)

        if instance.date_end_yesterday:
           events = events.filter(end_date__lte=now - timedelta(days=1))
        elif instance.date_end:
            events = events.filter(end_date__lte = instance.date_end)

        # Default
        if not instance.date_start_today and not instance.date_end_yesterday and instance.date_start == None and instance.date_end == None:
            events = events.filter(end_date__gte=now - timedelta(days=1))

        if instance.display_date_as == "descending":
            events = events.order_by("-event_date")
        else:
            events = events.order_by("event_date")

        if (instance.tags):
            filters = []
            for tag in instance.tags.split(','):
                filters.append(tag.strip())
            events = events.filter(tags__name__in = filters).distinct()

        if instance.calendars.count() > 0:
            calendar_filters = []
            for calendar in instance.calendars.all():
                calendar_filters.append(Q(calendar = calendar))
            events = events.filter(reduce(operator.or_, calendar_filters))

        context['more'] = instance.more
        context['events_list'] = events[:instance.limit]
        context['display_as'] = instance.display_as
        #self.render_template = instance.display
        return context


plugin_pool.register_plugin(EventsPlugin)
