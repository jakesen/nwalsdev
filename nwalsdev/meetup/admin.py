from django.contrib import admin
from nwalsdev.meetup.models import Location, Meetup

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Location, LocationAdmin)

class MeetupAdmin(admin.ModelAdmin):
    pass
admin.site.register(Meetup, MeetupAdmin)
