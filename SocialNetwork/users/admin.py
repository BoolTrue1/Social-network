from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'birth_date']

admin.site.register(UserProfile, UserProfileAdmin)