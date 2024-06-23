from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf.urls import handler404
from django.shortcuts import render
from . import views

from users.views import profile, edit_profile, people, friends


urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('add_friend/<str:username>/', views.add_friend, name='add_friend'),
    path('dialogs/', views.dialogs_view, name='dialogs'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile', profile, name='profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('people', people, name='people'),
    path('friends', friends, name='friends'),
    
    path('users/', include('users.urls')),
]


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

handler404 = custom_404