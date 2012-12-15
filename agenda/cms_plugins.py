from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _

from events.models import Event, Calendar, EventsPluginModel

class EventsPlugin(CMSPluginBase):
    model = EventsPluginModel
    name = _("Events")
    render_template = "events_plugin.html"
    
    def render(self, context, instance, placeholder):
        events = Event.objects.all()
        
        if (instance.tags):
            filters = []
            for tag in instance.tags.split(','):
                filters.append(tag.strip())
            events = events.filter(tags__name__in = filters).distinct()
        
        if (instance.calendar):
            events = events.filter(calendar=instance.calendar)
        
        context['events_list'] = events[:instance.limit]
        context['display_as'] = instance.display_as
        return context


plugin_pool.register_plugin(EventsPlugin)