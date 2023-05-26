from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class CustomUserCreationForm(forms.Form):
    fullname = forms.CharField()
    phone = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("fullname", "phone", "email",)
