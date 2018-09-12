from __future__ import absolute_import
from django.shortcuts import render

from events.library import query_events, parse_date_range

from plaza2.apps.bloat.library import paginate
from plaza2.apps.tagfilters.library import split_tags_list

def by_tags(request, calendar_list=None, tag_list=None, ordering="ascending",
            start_date_range='all', end_date_range='all', page=1):

    tags = split_tags_list(tag_list)
    calendars = split_tags_list(calendar_list)
    start_date_filters = parse_date_range(start_date_range)
    end_date_filters = parse_date_range(end_date_range)

    events = query_events(calendars=calendars, tags=tags, ordering=ordering,
                          min_start_date=start_date_filters[0], max_start_date=start_date_filters[1],
                          min_end_date=end_date_filters[0], max_end_date=end_date_filters[1])

    events = paginate(events, page=page)
    #print "Query (post-ordering): %s" % events.all()

    context = {
        'event_list': events,
        'calendars_str': calendar_list,
        'tags_str': tag_list,
        'ordering_str': ordering,
        'start_date_str': start_date_range,
        'end_date_str': end_date_range,
    }

    return render(request, 'events/event_archive.html', context)
