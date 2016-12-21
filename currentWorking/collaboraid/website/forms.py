from django import forms
from website.models import UserProfile, AnEvent

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    picture = forms.ImageField(required=False)
    
    class Meta:
        model = UserProfile
        exclude = ('user',)
        
class AnEventForm(forms.ModelForm):
    event_name = forms.CharField(required=True)
    picture = forms.ImageField(required=False)
    description = forms.CharField(required=True)
    volunteer_num = forms.IntegerField(required=True)

    venue = forms.CharField(required=True)
    address = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    
    date = forms.DateField(required=True)
    start_time = forms.TimeField(required=True)
    end_time = forms.TimeField(required=True)
    
    class Meta:
        model = AnEvent
        exclude = ('volunteer',)