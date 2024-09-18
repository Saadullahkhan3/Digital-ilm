from django.shortcuts import render
from django.contrib.auth.models import User 

def home(request):
    tutor_username = None  
    ok = 0
    if request.user.is_authenticated:
        ok = 1
        tutor_username = request.user.username
    return render(request, 'home.html', {"ok": ok, "tutor_username": tutor_username})

