from django.contrib import admin

from django.utils.translation import ugettext as _

from models import *

from taggit.models import Tag
from plaza2.apps.tagfilters.models import TagFamily
from django.conf import settings

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

class EventAdminForm(forms.ModelForm):
    #tags = forms.ModelMultipleChoiceField(
    #    Tag.objects.all().order_by("name"),
    #    widget=FilteredSelectMultiple("tags", False),
    #    required=False)

    class Meta:
        model = Event
        fields = "__all__"
 
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'event_date', 'end_date', 'location', 'publish', 'calendar')
    list_display_links = ('title', )
    list_filter = ('event_date', 'publish', 'author', 'location', 'calendar')

    date_hierarchy = 'event_date'
    
    prepopulated_fields = {"slug": ("title",)}
    
    #search_fields = ('title', 'location__title', 'author__username', 'author__first_name', 'author__last_name', 'calendar')
    search_fields = ('title', 'location', 'author__username', 'author__first_name', 'author__last_name', 'calendar__name')

    fieldsets =  ((None, {'fields': ['title', 'slug', 'event_date', 'end_date', 'start_time', 'end_time', 'event_url', 'location', 'description', 'tags', 'calendar',]}),
                  (_('Advanced options'), {'classes' : ('collapse',),
                                           'fields'  : ('publish_date', 'publish', 'sites', 'author', 'allow_comments')}))
    filter_horizontal = ('tags',)
    
    form = EventAdminForm

    # This is a dirty hack, this belongs inside of the model but defaults don't work on M2M
    def formfield_for_dbfield(self, db_field, **kwargs):
        """ Makes sure that by default all sites are selected. """
        if db_field.name == 'sites': # Check if it's the one you want
            kwargs.update({'initial': Site.objects.all()})
         
        return super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            if not request.user.is_superuser:
                admin_tags = settings.SUPERUSER_TAGFAMILIES
                tagnames = TagFamily.objects.filter(name__in=admin_tags).values_list('tags__name', flat=True).distinct()
                kwargs["queryset"] = Tag.objects.exclude(name__in = tagnames)
        return super(EventAdmin, self).formfield_for_manytomany(db_field, request, **kwargs )
    
class CalendarAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
admin.site.register(Event, EventAdmin)
admin.site.register(Calendar, CalendarAdmin)
