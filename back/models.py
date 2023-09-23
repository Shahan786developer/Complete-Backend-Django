from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomPhoneNumberField(PhoneNumberField):
    default_validators = []


class UserProfile(AbstractUser):
    phone_number = CustomPhoneNumberField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)  # Field for retype password
    pins = models.CharField(max_length=4)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
