# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# for User Manager:
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# for Messages:
from django.contrib import messages
# for regular expressions:
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def register(request):
    # Just show the registratoin page
    return render(request, 'session_words/register.html')

def doRegistration(request):
    if request.method == 'POST':
    # step 1: get the values out of the form posting
        userName = request.POST["username"]
        password = request.POST["password"]
        pwConfirm = request.POST["password_confirm"]
        email = request.POST["email"]
        firstName = request.POST["first_name"]
        lastName = request.POST["last_name"]

    # step 2: do some validations 
        isValid = True

        # First Name - Required; No fewer than 2 characters; letters only
        if len(firstName) > 2 :
            if not firstName.isalpha():
                messages.error(request, "First name cannot contain numbers.")
                isValid = False
        else:
            messages.error(request, "First name must be greater than 2 characters.")
            isValid = False
            
        # Last Name - Required; No fewer than 2 characters; letters only
        if len(lastName) > 2:
            if not lastName.isalpha():
                messages.error(request, "Last name cannot contain numbers.")
                isValid = False
        else:
            messages.error(request, "Last name must be greater than 2 characters.")
            isValid = False

        # Email - Required; Valid Format
        if not EMAIL_REGEX.match(email):
            messages.error(request, "Email format is not valid.")
            isValid = False

        # Password - Required; No fewer than 8 characters in length; matches Password Confirmation
        if len(password) < 8:
            messages.error(request, "Passwords must be at least 8 characters in length")
            isValid = False

        if password != pwConfirm:
            messages.error(request, "Passwords do not match!")
            isValid = False


        # Bonus: Birthday Field - Before today, or go creative and do it in an age range


    # step 3: decide what to do based on results of validations
        if isValid:
        # if we are in a valid state, we can create the new user, set session info and proceed.
            
            #user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

            # At this point, user is a User object that has already been saved
            # to the database. You can continue to change its attributes
            # if you want to change other fields.

            # user.last_name = 'Lennon'
            # user.save()

            user = User.objects.create_user(userName, email, password)
            # print "initial user name set as: ", user.username
            user.last_name = lastName
            user.first_name = firstName
            user.save()

            #send all user info to the template so we can view them
            context = {"allUsers" : User.objects.all()}

            return render(request, 'session_words/index.html', context)
        else:
            messages.warning(request, 'Registration has failed. Please correct the issues and try again.')
            
            #return render(request, 'session_words/register.html')
            return redirect("/")

def login(request):
    userName = request.POST["userName"]
    password = request.POST["password"]
    
    user = authenticate(username=userName, password=password)

    if user is not None:
        # A backend authenticated the credentials
        #send all user info to the template so we can view them
        context = {"allUsers" : User.objects.all()}
        messages.success(request, "You have logged in sucessfully, have a nice day")
        request.session["logged_in_user"] = user.username
        return render(request, 'session_words/index.html', context)
    else:
        # No backend authenticated the credentials
        messages.error(request, "User Name not found in the system. Please try again")
        return redirect("/")
    
    
def index(request):
    if "logged_in_user" not in request.session:
        messages.error(request, "please log in to view this page")
        return redirect('/')

    if 'words' not in request.session:
        request.session['words'] = []
    return render(request, 'session_words/index.html')

def add_word(request):
    if request.method == 'POST':
        input_keys = ['word', 'color', 'size']
        word = {}
        for key in input_keys:
            if key in request.POST:
                word[key] = request.POST[key]
        
        if len(word['word']) > 0:
            request.session['words'].append(word)
            request.session.modified = True
        
    return redirect('/')

def clear_words(request):
    request.session.clear()
    return redirect('/')
    
