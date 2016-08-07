# nwalsdev

Website for Northwest Alabama Software Developers

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
./manage.py runserver
```

## What we need

- Signin (social-auth)
	- User levels? (or, basically, who can create events to calendar?)
- Calendar with upcoming events
	- RSVP
- Email notifications
	- Confirmation
	- Reminder
	- Upcoming events?