from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, UserManager, Trip, TripManager
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password= password)
        request.session['uid']= user.id
        return redirect('/dashboard')
    
    
    
        
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, 'Email and password did not match')
            
    else:
        messages.error(request, 'Email is not registered')
    return redirect('/')


# dashboard method
def dashboard(request):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        context = {
            'logged_user': User.objects.get(id=request.session['uid']),
            'all_trips': Trip.objects.all()
        }
        return render(request, 'dashboard.html', context)



# create a new trip
def create_trip(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        new_trip = Trip.objects.create(destination= request.POST['destination'], start_date = request.POST['start_date'],
                                       end_date = request.POST['end_date'], plan = request.POST['plan'],
                                       poster  = User.objects.get(id=request.session['uid']))
        return redirect('/dashboard')
    return redirect('/trips/new')

# new trip page
def new_trip(request):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        context = {
            'logged_user': User.objects.get(id=request.session['uid']),
        }
        return render(request, 'new_trip.html', context)

#delete trip
def destroy(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        Trip.objects.get(id=id).delete()
        return redirect('/dashboard')


# edit trip
def edit_trip(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        context={
            'edit_trip': Trip.objects.get(id=id),
        }
        
        return render(request, 'edit.html', context)


# update trip
def update(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            str_id=str(id)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/trips/edit/{str_id}')
        else:
            str_id=str(id)
            edit_trip=Trip.objects.get(id=id)
            edit_trip.destination=request.POST['destination']
            edit_trip.plan=request.POST['plan']
            edit_trip.start_date=request.POST['start_date']
            edit_trip.end_date=request.POST['end_date']
            edit_trip.save()
        
        return redirect('/dashboard')
        
    return redirect('/dashboard')

# show one trip
def one_trip(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        trip= Trip.objects.get(id=id)

        context={
            'viewed_trip': Trip.objects.get(id=id),
            'logged_user': User.objects.get(id=request.session['uid']),
            'joined_users': User.objects.filter(has_joined__id=trip.id).exclude(id=trip.poster.id),
            
        }
        
        return render(request, 'one_trip.html', context)


# join a trip
def join_trip(request, trip_id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['uid'])
        trip = Trip.objects.get(id=trip_id)
        
        user.has_joined.add(trip)
        
        return redirect('/dashboard')


# delete join
def delete_join(request, trip_id):
    if 'uid' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['uid'])
        trip = Trip.objects.get(id=trip_id)
        
        user.has_joined.remove(trip)
        
        return redirect('/dashboard')

# log out 
def log_out(request):
    request.session.clear()
    return redirect('/')