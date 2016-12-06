from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.EmailField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username
    

    
class AnEvent(models.Model):
    event_name = models.CharField(max_length=30)
    venue = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=30)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='event_images', blank=True)
    description = models.TextField(max_length=400)
    
    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.event_name