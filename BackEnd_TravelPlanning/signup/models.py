from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None, birth_date=None, city=None, gender=None, **extra_fields):
        if not name or not email or not birth_date or not city or not gender: 
            raise ValueError('Users must have all fields') 
        email = self.normalize_email(email)
        user = self.model(
            name=name,
            email=email,
            birth_date=birth_date,
            city=city,
            gender=gender,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, birth_date=None, city=None, gender=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(name, email, password, birth_date, city, gender, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    female = 'Female'
    male = 'Male'
    choice = [
        ('Female',female),
        ('Male',male)
    ]
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    birth_date = models.DateField()
    city = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=choice)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'birth_date', 'city', 'gender']

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.email
