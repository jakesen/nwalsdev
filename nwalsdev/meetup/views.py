from django.shortcuts import render
from django.utils import timezone
from nwalsdev.meetup.models import Meetup

def upcoming(request):
    meetups = Meetup.objects.filter(start_time__gt=timezone.now())
    return render(request, 'meetup/upcoming.html', {'meetups': meetups})
