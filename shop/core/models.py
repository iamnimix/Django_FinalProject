from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjUserManager
from django.db import models


# Create your models here.


class UserManager(DjUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        pass


class User(AbstractUser):
    pass
