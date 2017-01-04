from django.contrib import admin
from nwalsdev.meetup.models import Location, Meetup

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Location, LocationAdmin)

def send_announcement_email(modeladmin, request, queryset):
    email_count = 0
    for meetup in queryset:
        email_count = email_count + meetup.send_announcement_email()
    message = str(email_count)+" emails sent"
    modeladmin.message_user(request, message)
send_announcement_email.short_description = "Send announcement email"

def test_announcement_email(modeladmin, request, queryset):
    email_count = 0
    for meetup in queryset:
        email_count = email_count + meetup.test_announcement_email()
    message = str(email_count)+" emails sent"
    modeladmin.message_user(request, message)
test_announcement_email.short_description = "Test announcement email (send to admins)"

class MeetupAdmin(admin.ModelAdmin):
    actions = (send_announcement_email, test_announcement_email)
admin.site.register(Meetup, MeetupAdmin)
