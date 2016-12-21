from django.contrib import admin
from website.models import UserProfile, AnEvent

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'venue', 'date', 'start_time', 'end_time')
    search_fields = ('event_name', 'venue', 'date',)
    

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(AnEvent, EventAdmin)
