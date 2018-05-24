from django.shortcuts import render, HttpResponse, redirect
from .models import User, Quote
from django.contrib import messages
import bcrypt
import re

def register(request):
    if request.method == "POST":
        errors = User.objects.registrationValidator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        else:
            pwHash = bcrypt.hashpw(request.POST['password'].encode('utf8'), bcrypt.gensalt())
            newUser = User.objects.create(firstName = request.POST['firstName'], lastName = request.POST['lastName'], userName = request.POST['userName'], email = request.POST['email'], password = pwHash)
            newUser.save()
            messages.success(request, "REGISTRATION WAS A SUCCESS NOW YOU MUST LOG IN")
            return redirect('/')

    return redirect ('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.loginValidator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        x = User.objects.get(userName = request.POST['loginUserName'])
        request.session['userID'] = x.id
        request.session['user'] = x.firstName
    return redirect ('/quotes')

def logout(request):
    request.session.flush()
    return redirect ('/')

def index(request):
    if 'user' in request.session:
        return redirect ('/quotes')

    return render (request, 'Exam/index.html')

def quotes(request):
    if 'user' not in request.session:
       return redirect ('/')

    context = {
        "user" : request.session['user'],
        "allQuotes" : Quote.objects.all(),
        "userID": request.session['userID']
    }
    return render (request, "Exam/quotes.html", context)

def addQuote(request):
    if 'user' not in request.session:
        return redirect ('/')

    context = {
        "user" : request.session['user']
    }
    if request.method == "POST":
        errors = User.objects.quoteValidator(request.POST)

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quotes')

        thisUser = User.objects.filter(id = request.session['userID']).first()
        newQuote = Quote.objects.create(author = request.POST['author'], quoteContent = request.POST['quote'], postedBy = thisUser)
        newQuote.save()
        return redirect ('/quotes')

    return render (request, "Exam/quotes.html", context)

def userQuotes(request, id):
    if 'user' not in request.session:
        return redirect ('/')
    context = {
        "thisUser" : User.objects.filter(id = request.session['userID']).first(),
        "thatUser" : User.objects.filter(id = id).first(),
        "quotes" : Quote.objects.filter(postedBy = id),
        "userID" : User.objects.filter(id = request.session['userID']).first().id
    }
    return render (request, "Exam/userQuotes.html",context)


def like (request, id):
    quoteToBeLiked = Quote.objects.filter(id = id).first()
    thisUser = User.objects.filter(id = request.session["userID"]).first()

    if thisUser.id not in quoteToBeLiked.likedBy.all():
        quoteToBeLiked.likedBy.add(thisUser)
        quoteToBeLiked.save()

    return redirect ('/quotes')

def editAccount(request):
    if 'user' not in request.session:
        return redirect ('/')
    if request.method == "POST":
        errors = User.objects.updateValidator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/editAccount')
        thisUser = User.objects.filter(id = request.session['userID']).first()
        thisUser.firstName = request.POST['firstName']
        thisUser.lastName = request.POST['lastName']
        thisUser.email = request.POST['email']
        thisUser.save()
        request.session['user'] = thisUser.firstName
        request.session['userID'] = thisUser.id
        messages.success(request, "INFO HAS BEEN UPDATED")
    context = {
        'thisUser': User.objects.filter(id = request.session["userID"]).first()
    }

    return render (request, "Exam/editAccount.html", context)

def delete(request, id):
    quoteToBeDeleted = Quote.objects.filter(id = id).first()
    quoteToBeDeleted.delete()
    return redirect('/quotes')