from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from .models import Meetup, RSVP
from .forms import RSVPForm

def upcoming(request):
    return render(request, 'meetup/upcoming.html')

def details(request, meetup_id):
    meetup = get_object_or_404(Meetup, pk=meetup_id)
    return render(request, 'meetup/details.html', { 'meetup': meetup, 'site': Site.objects.get_current() })

@login_required
def rsvp(request, meetup_id):
    meetup = get_object_or_404(Meetup, pk=meetup_id)
    rsvp, created = RSVP.objects.get_or_create(meetup=meetup, user=request.user)
    if request.method == "POST":
        rsvp_form = RSVPForm(request.POST, instance=rsvp)
        if rsvp_form.is_valid():
            rsvp_form.save()
            return HttpResponseRedirect(meetup.get_absolute_url())
    else:
        rsvp_form = RSVPForm(instance=rsvp)
    return render(request, 'meetup/rsvp.html', { 'meetup': meetup, 'rsvp_form': rsvp_form })
