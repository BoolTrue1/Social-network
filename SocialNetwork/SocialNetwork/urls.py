from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from users.views import profile, edit_profile, people


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile', profile, name='profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('people', people, name='people'),
    
    path('users/', include('users.urls')),
]
