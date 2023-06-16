from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from .manager import MyUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.

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

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        return self.phone
