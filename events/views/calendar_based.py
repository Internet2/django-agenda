from events.models import Event, Calendar

from django.shortcuts import get_object_or_404, render

def calendar_detail(request, slug):
    print "sLUG " + slug
    cal = get_object_or_404(Calendar, slug=slug)
    events = Event.objects.filter(calendar=cal)
    
    return render(request, 'events/calendar_detail.html', {
        'calendar': cal,
        'event_list': events
    })