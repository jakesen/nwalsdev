from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site

class Location(models.Model):
    name = models.CharField(max_length=254)
    address = models.CharField(max_length=254, blank=True)
    city = models.CharField(max_length=254, blank=True)
    state = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.name

    def full_address(self):
        return self.address+' '+self.city+' '+self.state


class Meetup(models.Model):
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location)
    start_time = models.DateTimeField()

    def test_announcement_email(self):
        return self.send_announcement_email(User.objects.filter(is_superuser=True))

    def send_announcement_email(self, recipient_users=User.objects.all()):
        site = Site.objects.get_current()
        plain_body = render_to_string('meetup/emails/announcement.txt', { 'site': site, 'meetup': self })
        html_body = render_to_string('meetup/emails/announcement.html', { 'site': site, 'meetup': self })
        email_count = 0
        for user in recipient_users:
            email = EmailMultiAlternatives(
                "New Meetup: "+self.title,
                plain_body,
                None, # use settings.DEFAULT_FROM_EMAIL
                [user.email]
            )
            email.attach_alternative(html_body, "text/html")
            email.send()
            email_count += 1
        return email_count

    def attendee_count(self):
        attendees = self.rsvp_set.filter(attending=True)
        guest_count = attendees.aggregate(Sum('additional_guests'))['additional_guests__sum']
        if guest_count:
            return attendees.count() + guest_count
        else:
            return attendees.count()

    def attendee_list(self):
        attendee_names = []
        for rsvp in self.rsvp_set.filter(attending=True).select_related('user'):
            if rsvp.user.get_full_name() != '':
                name = rsvp.user.get_full_name()
            else:
                name = rsvp.user.username
            if rsvp.additional_guests > 0:
                attendee_names.append(name+' + '+str(rsvp.additional_guests)+' guests')
            else:
                attendee_names.append(name)
        return attendee_names

    def get_absolute_url(self):
        return '/meetups/'+str(self.id)+'/'

    def __str__(self):
        return self.title

class RSVP(models.Model):
    meetup = models.ForeignKey(Meetup)
    user = models.ForeignKey(User)
    attending = models.BooleanField(default=False)
    additional_guests = models.IntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name()
