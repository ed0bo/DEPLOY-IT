from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt
import re

def index(request):
    return render (request, 'LoginRegistration/index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.registrationValidator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            pwHash = bcrypt.hashpw(request.POST['password'].encode('utf8'), bcrypt.gensalt())
            x = User.objects.create(firstName = request.POST['firstName'], lastName = request.POST['lastName'], userName = request.POST['userName'], email = request.POST['email'], password = pwHash)
            x.save()
            messages.success(request, "REGISTRATION WAS A SUCCESS NOW YOU MUST LOG IN")
            return redirect('/')
    return redirect ('/')

def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(userName = request.POST['loginUserName'])
        except:
            messages.success(request, "Make sure login info is correct plz")
            return redirect ('/')
        if bcrypt.checkpw(request.POST['loginPassword'].encode('utf-8'), user.password.encode('utf-8')):
            return render (request, "LoginRegistration/success.html")
        else:
            messages.success(request, "Make sure login info is correct plz")
            return redirect ('/')

    return render (request, 'LoginRegistration/index.html')

def success(request):
    return render (request, "LoginRegistration/success.html")