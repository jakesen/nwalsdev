from django import template
from django.utils import timezone
from datetime import timedelta
from nwalsdev.meetup.models import Meetup


register = template.Library()


@register.filter
def upcoming_meetups(user):
    if user.is_authenticated():
        two_hours = 2 * 60 * 60
        return Meetup.objects.filter(start_time__gt=timezone.now()-timedelta(seconds=two_hours))

@register.filter
def attending(user, meetup):
    if user.is_authenticated():
        for rsvp in user.rsvp_set.filter(meetup=meetup)[:1]:
            return rsvp.attending
    return False
