from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from dateutil import parser
from datetime import datetime

import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')


# Create your models here.
class UserManager(models.Manager):
    def validate_registration_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []

        if len(post_data['name']) < 3:
            errors.append("Name must be at least 3 characters long")

        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('Name may only contain characters')

        if len(post_data['user_name']) < 3:
            errors.append("User name must be at least 2 characters long")

        if not re.match(NAME_REGEX, post_data['user_name']):
            errors.append('user name may only contain characters')

        if len(post_data['password']) < 8:
            errors.append("Password must be at least 8 characters long")


        if post_data['password'] != post_data['pw_confirm']:
            errors.append("Invalid Password!")

        print " before error check" + str(errors)
        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            user = User.objects.create(
                        name       = post_data['name'],
                        user_name      = post_data['user_name'],
                        password   = hashedpwd)
            user.save()
            
            response['user'] = user

            print " after user " + str(user)
            
        return response

    def validate_login_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []
        hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

        user = User.objects.filter(user_name = post_data['user_name'])

        if len(user) > 0:
            # check this user's password
            user = user[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('user name/password incorrect')
        else:
            errors.append('user name/password incorrect')

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            response['user'] = user
        return response

    def validate_trip_data(self, post_data, user):
    	response = {
            'status' : True
        }
        errors = []
        print "********************"+ str(len(post_data['travel_date_from'])) + "$$$$$$$$$$$$$$$"+ post_data['travel_date_to']

        if len(post_data['destination']) == 0:
            errors.append("Destination can not be empty")
        if len(post_data['description']) == 0:
            errors.append("Description can not be empty")
        if len(post_data['travel_date_from']) == 0:
            errors.append("travel date should not be empty")
        if len(post_data['travel_date_to']) == 0:
            errors.append("travel end date should not be empty")
        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
        	start_dt = parser.parse(post_data['travel_date_from'])
        	end_dt = parser.parse(post_data['travel_date_to'])
        	#check if start data is less than current date fail validation
        	if start_dt < datetime.now():
        		errors.append("travel date should be greater than today")
        	#check end date is less than start date fail validation
        	elif end_dt < start_dt:
        		errors.append("travel end date should be greater than travel start date")
        	else:
	        	#else create object
    	   	    trip_data = Trip.objects.create(
        	        destination = post_data['destination'],
            	    desc      = post_data['description'],
                	start_date     = post_data['travel_date_from'],
                	end_date      = post_data['travel_date_to'])
    	   	    trip_data.save()
    	   	    trip_data.users.add(user)

            	response['trip_data'] = trip_data

        return response
 
# database models
class User(models.Model):
    name        = models.CharField(max_length=255)
    user_name       = models.CharField(max_length=255)
    password    = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    #trips = models.ManyToManyField(User, related_name="users") 
    objects     = UserManager()
    def __str__(self):
        return self.user_name
    

class Trip(models.Model):
    destination = models.CharField(max_length=255) 
    start_date = models.DateTimeField(verbose_name=('from datetime'))
    end_date = models.DateTimeField(verbose_name=('to datetime'))
    desc = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="trips")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = UserManager()
    def __str__(self):
        return self.destination