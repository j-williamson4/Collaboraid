
from django.conf.urls import url, include
from django.contrib import admin
from website import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^website/', include('website.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', views.WebsiteRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)