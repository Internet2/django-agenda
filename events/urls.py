from django.conf.urls import *

from models import *

from . import views
from views.date_based import *
from views.vobject_django import *
from views.custom import *


info_dict = {
    'queryset'                  : Event.published.all(),
    'date_field'                : 'event_date',
    'template_object_name'      : 'event',
}

urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', views.date_based.object_detail, info_dict,  name='agenda-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',                  views.date_based.archive,       info_dict,  name='agenda-archive-day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',                                   views.date_based.archive,       info_dict,  name='agenda-archive-month'),
    url(r'^(?P<year>\d{4})/$',                                                      views.date_based.archive,       info_dict,  name='agenda-archive-year'),
    url(r'^$',                                                                      views.date_based.index,         info_dict,  name='agenda-index'),
]

ical_dict = {
    'queryset'                  : info_dict['queryset'],
    'date_field'                : info_dict['date_field'],
    'ical_filename'              : 'calendar.ics',
    'last_modified_field'       : 'mod_date',
    'location_field'            : 'location',
    'start_time_field'          : 'start_time',
    'end_time_field'            : 'end_time',
}

urlpatterns += [
    url(r'^calendar.ics$',                                                          views.vobject_django.icalendar,     ical_dict,  name='agenda-icalendar'),
]

urlpatterns = [
    url(r'^by_tags/(?P<calendar_list>[^//]+)/(?P<tag_list>[^//]+)/(?P<ordering>[^//]+)/(?P<start_date_range>[^//]+)/(?P<end_date_range>[^//]+)/(?P<page>[^//]+)$', views.custom.by_tags),
]

