from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from website.models import UserProfile
from website.forms import UserProfileForm
from website.models import AnEvent
from website.forms import AnEventForm
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
                            'website': userprofile.website, 'picture': userprofile.picture })
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    
    return render(request, 'website/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})

@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()
    return render(request, 'website/list_profiles.html', { 'userprofile_list' : userprofile_list})



############################################

@login_required
def register_event(request):
    created = False
    if request.method == 'POST':
        event_form= AnEventForm(data=request.POST)
        
        if event_form.is_valid():
            event = event_form.save()
            event.save()
            created = True
            
            #profile = profile_form.save(commit=False)
            #profile.user = user
            #if 'picture' in request.FILES:
                #profile.picture = request.FILES['picture']
                #profile.save()
                #registered = True
        else:
            print(event_form.errors)
    else:    	
        event_form = AnEventForm()
    
    #form = AnEventForm()
    #if request.method == 'POST':
     #   form = AnEventForm(request.POST, request.FILES)
    #    if form.is_valid():
     #       event_profile = form.save(commit=False)
           # event_profile.event = request.event
    #        event_profile.save()
            
    #        return redirect('index')
    #   else:
    #        print(form.errors)

    context_dict = {'form':form}
    
    return render(request, 'website/event_registration.html', context_dict)

#class WebsiteRegistrationView(RegistrationView):
    #def get_success_url(self, user):
        #return reverse('register_profile')

#@login_required
#def profile(request, username):
    #try:
        #user = User.objects.get(username=username)
    #except User.DoesNotExist:
        #return redirect('index')
    
    #userprofile = UserProfile.objects.get_or_create(user=user)[0]
    #form = UserProfileForm({'first_name': userprofile.first_name, 'last_name': userprofile.last_name, 
                            #'website': userprofile.website, 'picture': userprofile.picture })
    
    #if request.method == 'POST':
        #form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        #if form.is_valid():
            #form.save(commit=True)
            #return redirect('profile', user.username)
        #else:
            #print(form.errors)
    
    #return render(request, 'website/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})

@login_required
def list_events(request):
    events_list = AnEvent.objects.all()
    return render(request, 'website/list_events.html', { 'events_list' : events_list})
