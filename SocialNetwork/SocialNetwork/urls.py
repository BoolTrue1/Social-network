from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf.urls import handler404
from django.shortcuts import render
from users import views
# from . import views

from users.views import profile, edit_profile, people, friends

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('add_friend/<str:username>/', views.add_friend, name='add_friend'),
    path('send_message/<str:username>/', views.send_message, name='send_message'),
    path('messages/', views.view_messages, name='messages'),
    path('album/<str:username>/', views.album_view, name='album'),
    path('photo/<int:album_id>/', views.photo_view, name='photo'),
    path('community/', views.community_view, name='community'),
    path('community/<int:community_id>/', views.community_detail_view, name='community_detail'),
    path('join_community/<int:community_id>/', views.join_community, name='join_community'),
    path('leave_community/<int:community_id>/', views.leave_community, name='leave_community'),
    path('admin/block_user/<int:user_id>/', views.admin_block_user, name='admin_block_user'),
    path('admin/unblock_user/<int:user_id>/', views.admin_unblock_user, name='admin_unblock_user'),
    path('admin/mute_user/<int:user_id>/', views.admin_mute_user, name='admin_mute_user'),
    path('admin/unmute_user/<int:user_id>/', views.admin_unmute_user, name='admin_unmute_user'),
    path('admin/delete_user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('dialogs/', views.dialogs_view, name='dialogs'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # path('', include('users.urls')),
    path('profile', profile, name='profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('people', people, name='people'),
    path('friends', friends, name='friends'),
    
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

handler404 = custom_404