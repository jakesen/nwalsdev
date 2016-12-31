from django import template
from django.utils import timezone
from datetime import timedelta
from nwalsdev.meetup.models import Meetup


register = template.Library()


@register.filter
def upcoming_meetups(user):
    if user.is_authenticated:
        two_hours = 2 * 60 * 60
        return Meetup.objects.filter(start_time__gt=timezone.now()-timedelta(seconds=two_hours))
