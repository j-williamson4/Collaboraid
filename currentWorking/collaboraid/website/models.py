from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import date, time
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username
    
class AnEvent(models.Model):
    event_name = models.CharField(max_length=50)
    
    picture = models.ImageField(upload_to='event_images', blank=True)
    description = models.TextField(max_length=400)
    volunteer_num = models.IntegerField(default=0)
        
    venue = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=30)
    
    volunteer = models.ManyToManyField(User, blank=True)

    date = models.DateField(default=date.today)
    start_time = models.TimeField(help_text='ex: 10:30 for 10:30 AM', default=datetime.time(00, 00))
    end_time = models.TimeField(help_text='ex: 13:30 for 1:30 PM', default=datetime.time(00, 00))

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.event_name