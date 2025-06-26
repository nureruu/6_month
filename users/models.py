from django.contrib.auth.models import AbstractUser, BaseUserManager, User, AbstractBaseUser, PermissionsMixin
from django.db import models
import random


class User(AbstractUser):
    pass

class CustomUserManager():
    def create_user(self, email, username=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password()
        user.save()
        return user
        
    def create_superuser(self, email, username=None, password=None **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff')is not True:
            raise ValueError("staff must have true ")
        if extra_fields.get('is_superuser')is not True:
            raise ValueError("superuser must have true ")
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    username_field = ""
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or ""

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation')
    code = models.CharField(max_length=6)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)
