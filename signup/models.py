<<<<<<< Updated upstream
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None,**extra_fields):
        if not user_name or not email : 
            raise ValueError('Users must have all fields') 
        email = self.normalize_email(email)
        user = self.model(
            user_name=user_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password=None, birth_date=None, city=None, gender=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_name, email, password,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, unique=True, default='yourname')
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')), blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

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
=======
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None,**extra_fields):
        if not user_name or not email : 
            raise ValueError('Users must have all fields') 
        email = self.normalize_email(email)
        user = self.model(
            user_name=user_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password=None, birth_date=None, city=None, gender=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_name, email, password,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, unique=True, default='yourname')
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')), blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    # current_password = models.CharField(max_length=10, blank=True, null=True)
    # new_password = models.CharField(max_length=10, blank=True, null=True)
    # confirm_password = models.CharField(max_length=10, blank=True, null=True)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

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
>>>>>>> Stashed changes
