import datetime
import dateutil.parser

from events.models import Event

def parse_date_range(range):
    if range == "all":
        return [ None, None ]

    fields = range.split(',')
    for index, field in enumerate(fields):
        if field != None and field != "":
            fields[index] = dateutil.parser.parse(field)
        else:
            fields[index] = None

    return fields

def output_date_range(range):
    if range[0] == None and range[1] == None:
        return "all"

    range_str = ""
    if range[0]:
        range_str += range[0].isoformat()
    range_str += ","
    if range[1]:
        range_str += range[1].isoformat()

    return range_str

def query_events(calendars=None, tags=None, ordering="ascending",
           start_date=None, end_date=None):

    events = Event.objects.all()

#    print "Query: %s" % events.all()

    if len(tags) > 0:
#        print "Events Tag List: %s" % tags
        events = events.filter(tags__slug__in=tags)

#    print "Query (post-tags): %s" % events.all()

    if len(calendars) > 0:
#        print "Calendar List: %s" % calendars
        events = events.filter(calendar__slug__in=calendars)

#    print "Query (post-calendars): %s" % events.all()

    if start_date and end_date:
        events = events.filter(Q(end_date__gte = start_date), Q(event_date__lte = end_date))
    elif start_date:
        events = events.filter(end_date__gte = start_date)
    elif end_date:
        events = events.filter(end_date__lte = end_date)

#    print "Query (post-dates): %s" % events.all()

    if ordering == "descending":
        events = events.order_by("-event_date")
    else:
        events = events.order_by("event_date")

    events = events.distinct()

#    print "Query (post-ordering): %s" % events.all()

    return events
