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
        events = events.filter(end_date__gte=now - timedelta(days=1)).order_by("-event_date")
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
        return context


plugin_pool.register_plugin(EventsPlugin)
