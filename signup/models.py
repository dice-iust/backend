from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string


class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None, **extra_fields):
        if not user_name or not email:
            raise ValueError("Users must have all fields")
        email = self.normalize_email(email)
        user = self.model(user_name=user_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        user_name,
        email,
        password=None,
        birth_date=None,
        city=None,
        gender=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(user_name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, unique=True, default="yourname")
    email = models.EmailField(max_length=100, unique=True)
    firstName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profilePicture = models.ImageField(
        upload_to="profile_pictures/",
        default="profile_pictures/photo_1_2024-11-22_00-36-00.jpg",
        blank=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
        blank=True,
        null=True,
    )
    bio = models.TextField(default="Hey! I'm using TripTide.")
    phone = models.CharField(max_length=15, blank=True, null=True)
    birthDate = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(blank=True, null=True, default=0)
    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions_set", blank=True
    )

    def __str__(self):
        return self.email


class EmailVerification(models.Model):
    verification_code = models.CharField(max_length=6)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # Fixed typo here
    email = models.EmailField()
    time_add = models.DateTimeField(default=timezone.now)
    token = models.CharField(max_length=32, null=True, blank=True)

    class Meta:

        unique_together = ("verification_code", "email")


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Password reset request for {self.user.email}"

    @staticmethod
    def generate_reset_code():
        return "".join(random.choices(string.digits, k=6))


class BlacklistedToken(models.Model):
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
