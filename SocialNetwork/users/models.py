from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    profile = models.TextField(blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    friends = models.ManyToManyField('self', blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username


