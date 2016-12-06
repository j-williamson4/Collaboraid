from django import forms
from website.models import UserProfile
from website.models import AnEvent

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False) 
    class Meta:
        model = UserProfile
        exclude = ('user',)
        
class AnEventForm(forms.ModelForm):
    event_name = forms.CharField(required=False)
    venue = forms.CharField(required=False)
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)
    description = forms.CharField(required=False)
    #date = forms.DateField(required=False)
    #time = forms.TimeField(required=False)
    
    class Meta:
        model = AnEvent
        exclude = ('event_name',)