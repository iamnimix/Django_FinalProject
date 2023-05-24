from django.contrib.auth.models import BaseUserManager


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
