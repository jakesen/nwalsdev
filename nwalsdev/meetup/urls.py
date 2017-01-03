from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^upcoming/$', views.upcoming),
    url(r'^(?P<meetup_id>[0-9]+)/$', views.details),
    url(r'^(?P<meetup_id>[0-9]+)/rsvp/$', views.rsvp),
]
