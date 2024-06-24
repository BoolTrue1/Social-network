from django.urls import path, include
from users.views import Register
from users import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('add_friend/<str:username>/', views.add_friend, name='add_friend'),
    path('dialogs/', views.dialogs_view, name='dialogs'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    
    path('register/', Register.as_view(), name='register'),
]