# models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

  

class Ambulance(models.Model):
    registration_number = models.CharField(max_length=20)
    ambulance_type = models.CharField(max_length=50)  # New field for ambulance type
    capacity = models.PositiveIntegerField()
    availability_status = models.BooleanField(default=True)
    current_location_latitude = models.FloatField()
    current_location_longitude = models.FloatField()

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    location_latitude = models.FloatField()
    location_longitude = models.FloatField()

class AmbulanceBooking(models.Model):
    your_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    pickup_location = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    AMBULANCE_CHOICES = [
        ('Basic Ambulance', 'Basic Ambulance'),
        ('Advanced Ambulance', 'Advanced Ambulance'),
        ('Intensive Care Unit (ICU) Ambulance', 'Intensive Care Unit (ICU) Ambulance'),
        ('Specialized Ambulance', 'Specialized Ambulance'),
    ]

    ambulance_type = models.CharField(max_length=100, choices=AMBULANCE_CHOICES)
    additional_comments = models.TextField()
   
    total_amount =  models.CharField(max_length=15)  # Default to 0 if not found

    
   

class Dispatcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
