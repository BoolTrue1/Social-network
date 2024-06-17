from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=35, blank=True)
    birth_date = models.DateField(blank=True)
    main_photo = models.FilePathField(blank=True)
    about_me = models.TextField(blank=True)