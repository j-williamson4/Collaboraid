from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from website.models import UserProfile, AnEvent
from website.forms import UserProfileForm, AnEventForm, SearchForm
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q

# Create your views here.

def index(request):
    response = render(request, 'website/index.html')
    
    return response
    
def about(request):
    return render(request, 'website/about.html',{})
    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
    else:    	
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'website/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered
                  })

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            
            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form':form}
    
    return render(request, 'website/profile_registration.html', context_dict)

class WebsiteRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'first_name': userprofile.first_name, 'last_name': userprofile.last_name, 
                            'picture': userprofile.picture })
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    
    return render(request, 'website/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})

@login_required
def register_event(request):
    form = AnEventForm()
    if request.method == 'POST':
        form = AnEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('created_event')
        else:
            print(form.errors)

    context_dict = {'form':form}
    
    return render(request, 'website/event_registration.html', context_dict)

@login_required
def join(request, event_id):
    try:
        # already joined
        event = AnEvent.objects.get(id=event_id, volunteer=request.user)
        message = "You have already joined this event"
    except AnEvent.DoesNotExist as e:
        # Event exists and join
        try:
            event = AnEvent.objects.get(id=event_id)
            event.volunteer.add(request.user)
            event.save()
            message = "You have joined this event"
        except AnEvent.DoesNotExist as e:
            message = "Error on event joining"

    event = AnEvent.objects.get(id=event_id)
    joined = event.volunteer.filter(id=request.user.id)
    return render(request, 'website/event_details.html', {
       'event': event,
       'message': message,
       'joined': joined
    })

@login_required
def cancel(request, event_id):
    try:
        event = AnEvent.objects.get(id=event_id, volunteer=request.user)
        event.volunteer.remove(request.user)
        event.save()
        message = "Your request not to attend has been saved"
    except AnEvent.DoesNotExist as e:
           message = "Error on cancelling your attedance on event"

    event = AnEvent.objects.get(id=event_id)
    joined = event.volunteer.filter(id=request.user.id)
    return render(request, 'website/event_details.html', {
        'event': event,
        'message': message,
        'joined': joined
    })

@login_required
def event_complete(request):
    response = render(request, 'website/creation_complete.html')
    
    return response
    
@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()
    return render(request, 'website/list_profiles.html', { 'userprofile_list' : userprofile_list})

@login_required
def list_events(request):
    event_list = AnEvent.objects.all()
    return render(request, 'website/list_events.html', { 'event_list' : event_list})
    
    #this currently displays NEW upcoming events
    #if no new events, then empty
    #try:
    #    event = AnEvent.objects.filter(date__gt=datetime.now()).order_by('date')
    #except:
    #    event = []
        
    #return render(request, 'website/list_events.html', {'event': event})

@login_required
def user_event(request, user_id):
   try:
       event_list = AnEvent.objects.filter(volunteer__id=user_id)
       user = User.objects.get(id=user_id)
   except:
       event_list = []
       user = {}

   return render(request, 'website/user_events.html', {'event_list': event_list, 'user': user})

# Provides individual event details
@login_required
def detail(request, id):
   event = AnEvent.objects.get(id=id)
   joined = event.volunteer.filter(id=request.user.id)
   return render(request, 'website/event_details.html', {'event': event, 'joined': joined})

@login_required
def search(request):
    results = AnEvent.objects.all()

    query = request.GET.get('q')
    
    if query:
        results = results.filter(
            Q(event_name__icontains=query)|
            Q(venue__icontains=query)|
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)
            ).order_by("date")

    context = {
        "query" : query,
        "results" : results
    }
    
    return render(request, "website/search.html", context)
    
@login_required
def user_search(request):
    
    res = UserProfile.objects.all()

    query = request.GET.get('q')

    if query:
        res = res.filter(
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query) |
            Q(id__icontains=query)
            ).order_by("user")

    context = {
        "query" : query,
        "res" : res
    }

    return render(request, "website/user_search_results.html", context)