from django.shortcuts import render

def upcoming(request):
    return render(request, 'meetup/upcoming.html')
