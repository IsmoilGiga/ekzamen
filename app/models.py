from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import timedelta
from django.conf import settings
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.update(is_staff=True, is_superuser=True, is_active=True)
        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    phone = models.CharField(max_length=12, unique=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class EmailVerification(models.Model):
    LIFETIME = timedelta(minutes=5)
    MAX_ATTEMPTS = 5

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    attempts = models.PositiveSmallIntegerField(default=0)
    is_confirmed = models.BooleanField(default=False)     # kod to'g'ri kiritildimi
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + self.LIFETIME


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class PhoneCode(models.Model):
    LIFETIME = timedelta(minutes=5)
    MAX_ATTEMPTS = 5

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    attempts = models.PositiveSmallIntegerField(default=0)
    is_confirmed = models.BooleanField(default=False)     # kod to'g'ri kiritildimi
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + self.LIFETIME