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
           min_start_date=None, max_start_date=None, min_end_date=None, max_end_date=None):

    events = Event.objects.all()

    print "Query: %s" % events.all()

    if len(tags) > 0:
        print "Events Tag List: %s" % tags
        events = events.filter(tags__slug__in=tags)

    print "Query (post-tags): %s" % events.all()

    if len(calendars) > 0:
        print "Calendar List: %s" % calendars
        events = events.filter(calendar__slug__in=calendars)

    print "Query (post-calendars): %s" % events.all()

    if min_start_date:
        events = events.filter(event_date__gte = min_start_date)
    if max_start_date:
        events = events.filter(event_date__lte = max_start_date)

    print "Query (post-start): %s" % events.all()

    if min_end_date:
        events = events.filter(end_date__gte = min_end_date)
    if max_end_date:
        events = events.filter(end_date__lte = max_end_date)

    print "Query (post-end): %s" % events.all()

    if ordering == "descending":
        events = events.order_by("event_date")
    else:
        events = events.order_by("-event_date")

    print "Query (post-ordering): %s" % events.all()

    return events
