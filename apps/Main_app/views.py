# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from ..User_app.models import User
from .models import Trip

def index(request):

    context = {
        "longintrip" : Trip.objects.filter(users__id = request.session["user_id"]),
        "othertrip" : Trip.objects.exclude(users__id = request.session["user_id"]),
        'users': User.objects.exclude(id=request.session['user_id']),
        
    }
    return render(request,"Main_app/index.html",context)



def add(request):

    return render(request,"Main_app/add.html")

def createtrip(request):

    trip = Trip.objects.create(
            name = request.POST['name'],
            desc = request.POST['desc'],
            td_from = request.POST['td_from'],
            td_to = request.POST['td_to'],
        )

    user = User.objects.get(id = request.session['user_id'])
    trip.users.add(user)
    
    return redirect('/main')

def join(request,trip_id):

    trip = Trip.objects.get(id = trip_id)
    user = User.objects.get(id = request.session['user_id'])
    trip.users.add(user)

    return redirect('/main')

def destination(request,trip_id):

    context = {
        "trips" : Trip.objects.filter(id = trip_id),
        "users" : User.objects.filter(trips__id=trip_id),
    }
    
    return render (request,"Main_app/destination.html",context)
# Create your views here.
