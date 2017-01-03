from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^upcoming/$', views.upcoming),
]
