# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from .models import User
from django.contrib import messages

def index(request):

    return render (request,"User_app/index.html")

def register(request):
    response = User.objects.add_user(request.POST)
    if response['status']:
        request.session['user_id'] = response['user'].id
        request.session['user_name'] = response['user'].name
        return redirect('/main')
    else:
        for error in response['errors']:
            messages.error(request, error)
    return redirect('/')

def login(request):
    response = User.objects.validate_user(request.POST)
    if response['status']:
        request.session['user_id'] = response['loggedin_user'].id
        request.session['user_name'] = response['loggedin_user'].name
        return redirect('/main')
    else:
        for error in response['errors']:
            messages.error(request, error)
    return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')

# Create your views here.
