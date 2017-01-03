from django.shortcuts import render, get_object_or_404

from .models import Meetup

def upcoming(request):
    return render(request, 'meetup/upcoming.html')

def details(request, meetup_id):
    meetup = get_object_or_404(Meetup, pk=meetup_id)
    return render(request, 'meetup/details.html', { 'meetup': meetup })
