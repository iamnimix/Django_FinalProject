from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager, UserManager
from django.db import models
from django.utils import timezone
from jdatetime import date as jdate, datetime as jdatetime


# Create your models here.

class JalaliDateField(models.DateField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if isinstance(value, jdate):
            return value.togregorian().date()
        return value

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, jdate):
            return value.togregorian().date()
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, jdatetime):
            return value.date()
        return value


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = JalaliDateField(auto_now=True)
    is_deleted = models.BooleanField('Is Deleted', default=False, null=False, blank=False)


class MyUserManager(BaseUserManager):
    def create_user(self, fullname, email, phone, password, **extra_fields):
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
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, fullname=None, email=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(fullname, email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(null=True, max_length=100)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
    )
    phone = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        return self.phone
