from django.db import models
import re
from datetime import datetime, date
import bcrypt



class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] ='Password should be at least 8 characters'
        if postData['password'] != postData['conf_password']:
            errors['conf_password'] = 'Passwords should match'         
        result = User.objects.filter(email=postData['email'])
        if len(result) > 0:
            errors['email'] = 'Email has already been registered!'
            
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        
        # basic validations 
        if len(postData['destination']) < 3 or postData['destination'] == '':
            errors["destination"] = "Destination can not be empty should be at least 3 characters"
        if len(postData['plan']) < 3 or postData['plan'] == " ":
            errors["plan"] = "Plan can not be empty and it should be at least 3 characters"
        # Start date must be in the future and end date should be after the start date
        
        if postData['start_date'] == "" or  postData['end_date']=="" :
            errors['start_date'] = "Start date or end date can not be empty!" 
        
       
        if postData['start_date'] < str(date.today()):
            errors['start_date'] = "Start date must be in the future"
        if postData['start_date'] > postData['end_date']:
            errors['end_date'] = 'End date should be after the start date'
            
        return errors
    
class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    poster=models.ForeignKey(User, related_name = "has_trips", on_delete=models.CASCADE)
    joined_by = models.ManyToManyField(User, related_name= 'has_joined')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    