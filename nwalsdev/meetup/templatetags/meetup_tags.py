from django import template
from django.utils import timezone
from datetime import timedelta
from nwalsdev.meetup.models import Meetup


register = template.Library()


@register.filter
def upcoming_meetups(user):
    two_hours_ago = timezone.now() - timedelta(seconds=2*60*60)
    upcoming_meetups = Meetup.objects.filter(start_time__gt=two_hours_ago)
    return upcoming_meetups.select_related('location').order_by('start_time')

@register.filter
def attending(user, meetup):
    if user.is_authenticated():
        for rsvp in user.rsvp_set.filter(meetup=meetup)[:1]:
            return rsvp.attending
    return False
