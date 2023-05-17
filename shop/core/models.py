from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, UserManager
from django.db import models


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, fullname, email, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an phone number")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            fullname=fullname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, email, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            fullname=fullname,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
    )
    phone = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ['fullname', 'email']

    def has_perm(self, perm, obj=None):
        # Check if the user has a specific permission
        return True

    def has_module_perms(self, app_label):
        # Check if the user has permissions to view the app
        return True

    @property
    def is_staff(self):
        # Check if the user is a staff member
        return self.is_admin
