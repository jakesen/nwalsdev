from django.test import TestCase
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
        test_meetup = Meetup(
            title="Coders Lunch",
            location=test_location,
            start_time=timezone.now()+timedelta(days=1)
        )
        test_meetup.save()

        #self.client = Client()

    def test_upcoming(self):
        response = self.client.get("/upcoming/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Coders Lunch")
        self.assertContains(response,"123 Main Street")
