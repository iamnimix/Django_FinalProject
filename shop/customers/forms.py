from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("fullname", "phone", "email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("fullname", "phone", "email",)