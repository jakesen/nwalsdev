from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core import mail
from nwalsdev.meetup.models import Location, Meetup, RSVP
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

        rsvp_user = User.objects.create(username="jill", email="jill@nwalsdev.org")
        rsvp = RSVP.objects.create(
            meetup=self.test_meetup,
            user=rsvp_user,
            attending=True,
            additional_guests=2
        )

        test_user = User(username="joe", email="joe@nwalsdev.org", is_superuser=True)
        test_user.set_password('password')
        test_user.save()

        self.client = Client()

    def test_upcoming(self):
        response = self.client.get("/meetups/upcoming/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Coders Lunch")
        self.assertContains(response,"123 Main Street")
        self.assertContains(response,"3 coders")

    def test_details(self):
        meetup_url = self.test_meetup.get_absolute_url()
        # result contains meetup details without attendee list
        response = self.client.get(meetup_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Coders Lunch")
        self.assertContains(response,"123 Main Street")
        self.assertContains(response,"3 coders")
        self.assertNotContains(response,"jill + 2 guests")
        # result contains meetup attendee list if user is authenticated
        self.client.login(username='joe', password='password')
        response = self.client.get(meetup_url)
        self.assertContains(response,"jill + 2 guests")

    def test_rsvp(self):
        meetup_url = self.test_meetup.get_absolute_url()
        rsvp_url = meetup_url+'rsvp/'
        # requires login
        response = self.client.get(rsvp_url)
        self.assertEqual(response.status_code, 302)
        # returns rsvp form if user is authenticated
        self.client.login(username='joe', password='password')
        response = self.client.get(rsvp_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Coders Lunch")
        # saves rsvp values
        self.client.post(rsvp_url, { 'attending':True, 'additional_guests':0 })
        attending_users = self.test_meetup.rsvp_set.filter(attending=True).count()
        self.assertEqual(attending_users, 2)
        # rsvp status is reflected in details
        response = self.client.get(meetup_url)
        self.assertContains(response,"RSVP'd")

    def test_announcement_email(self):
        # Send message.
        self.assertEqual(self.test_meetup.send_announcement_email(), 2)
        # Test that one message has been sent to each user
        self.assertEqual(len(mail.outbox), User.objects.all().count())
        # Verify that the subject and body of the first message is correct.
        self.assertEqual(
            mail.outbox[0].subject,
            "Invitation: Coders Lunch"
        )

    def test_announcement_email_test(self):
        # Send message.
        self.assertEqual(self.test_meetup.test_announcement_email(), 1)
        # Test that one message has been sent to each user
        self.assertEqual(len(mail.outbox), User.objects.filter(is_superuser=True).count())
