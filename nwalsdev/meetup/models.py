from __future__ import unicode_literals

from django.db import models

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

    def __str__(self):
        return self.title
