from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("phone", "email", "fullname", "is_staff", "is_active",)
    list_filter = ("phone", "email", "fullname", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("fullname", "phone", "password", "email")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "fullname", "phone", "email", "password1", "password2", "is_staff",
                "is_superuser", "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("phone",)
    ordering = ("phone",)


admin.site.register(User, CustomUserAdmin)
