from django.shortcuts import render, HttpResponse, redirect
# the index function is called when root is visited
from .models import User
from .models import Trip
import datetime


def index(request):
    response = "Hello, I am your first request!"
    return render(request,'test_app/index.html')

def create_user(request):
    # the method validate_registration_data validates the form data and if there
    # are no errors, it also creates the user and returns the user object.
    # if there are errors, it returns a list of them in the response object.
    print "I am in index of user create ***"
    response = User.objects.validate_registration_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        request.session['name']    = response['user'].name
        request.session['user_name'] = response['user'].user_name
        request.session['user_id'] = response['user'].id
        user_name = request.session['user_name'] 
        print "in if statement***"
        return render(request, "test_app/travels.html")
    else:
        print "in else statement***"
        request.session['errors'] = response['errors']
        return render(request, "test_app/travels.html")

def user_login(request):
    
    # the method validate_registration_data validates the form data and if there
    # are no errors, it also creates the user and returns the user object.
    # if there are errors, it returns a list of them in the response object.

    print "I am in login page ***"

    response = User.objects.validate_login_data(request.POST)

    if (response['status']):
        request.session['name']    = response['user'].name
        request.session['user_name'] = response['user'].user_name
        request.session['user_id'] = response['user'].id
        request.session['errors']  = []
        user_id = request.session['user_name'] 
        #return redirect('/user/{}'.format(user_id))
        return redirect("/travels")
    else:
        request.session['errors'] = response['errors']
        return redirect('/')

def travels(request):

	user = User.objects.get(id= request.session['user_id'])
	#get travel list for user
	currentDT = datetime.datetime.now()
	print "#########" +(str(currentDT))
	user_trips=user.trips.filter(start_date__gte = currentDT)

	print "^^^^^^^^^" + str(user_trips.values())	

	#get travel list of other users matching same start and end dates
	print "(((((((((" + user.user_name
	all_user_trips = Trip.objects.filter(start_date__gte = currentDT).exclude(users__user_name = user.user_name)

	#create a context object with user_travel_list and other_users_travel_list and pass this to travels html page
	context = {
			"user_trips" : user_trips,
			"all_user_trips" : all_user_trips,
			"user_name": user.user_name
	}
	return render(request, "test_app/travels.html", context)

def add_trip_get(request):
	return render(request, "test_app/add_trip.html")

def add_trip_post(request):

	# get validated data from form 
	print "I am in user add trip method ***"
	user = User.objects.get(id= request.session['user_id'])
	response = Trip.objects.validate_trip_data(request.POST, user)

	if (response['status']):
		#set sessions
		print "I am in if"
	else:
		request.session['errors'] = response['errors']
		return redirect('/add_trip_get')



def join_trip(request, trip_id):
	#retrive user info session user id
	user = User.objects.get(id= request.session['user_id'])

	#retrieve trip info from trip id
	trip = Trip.objects.get(id = trip_id)

	#assign user to the trip using trip.users.add()
	trip.users.add(user)
	trip.save()

	return redirect('/travels')

def trip_details(request, trip_id):
	#retrive user info session user id
	user = User.objects.get(id= request.session['user_id'])

	#retrieve trip info from trip id
	trip = Trip.objects.get(id = trip_id)

	context = {
			
			"trip" : trip,
			"user_name": user.name
	}
	return render(request, "test_app/destination.html", context)

def log_out(request):
	request.session.clear()	
	
	return redirect('/')
	