from django.test import TestCase, Client
from django.contrib.auth.models import User
from nwalsdev.meetup.models import Location, Meetup
from datetime import timedelta
from django.utils import timezone

class TestMeetups(TestCase):
    def setUp(self):
        test_location = Location(
            name="City Hardware",
            address="123 Main Street"
        )
        test_location.save()
        self.test_meetup = Meetup(
            title="Coders Lunch",
            location=test_location,
            start_time=timezone.now()+timedelta(days=1)
        )
        self.test_meetup.save()

        test_user = User(username="joe")
        test_user.set_password('password')
        test_user.save()

        self.client = Client()

    def test_upcoming(self):
        response = self.client.get("/meetups/upcoming/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Coders Lunch")
        self.assertContains(response,"123 Main Street")

    def test_details(self):
        response = self.client.get(self.test_meetup.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Coders Lunch")
        self.assertContains(response,"123 Main Street")

    def test_rsvp(self):
        rsvp_url = self.test_meetup.get_absolute_url()+'rsvp/'
        # requires login
        response = self.client.get(rsvp_url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='joe', password='password')
        response = self.client.get(rsvp_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Coders Lunch")
        # saves rsvp values
        self.client.post(rsvp_url, { 'attending':True, 'additional_guests':0 })
        attending_users = self.test_meetup.rsvp_set.filter(attending=True).count()
        self.assertEqual(attending_users, 1)
