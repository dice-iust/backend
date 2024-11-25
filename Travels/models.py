from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Travel(models.Model):
    TYPE_CHOICES = [("Budget-friendly", "Budget-friendly"), ("Fancy", "Fancy")]
    TRANS_CHOICES = [
        ("Train", "Train"),
        ("Bus", "Bus"),
        ("Plane", "Plane"),
        ("Car", "Car"),
    ]

    admin = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="admin_trips"
    )
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    photo = models.ImageField(upload_to="profiles", blank=True)
    destination = models.CharField(max_length=200)
    mode = models.CharField(max_length=200, choices=TYPE_CHOICES)
    start_place = models.CharField(max_length=200)
    transportation = models.CharField(max_length=200, choices=TRANS_CHOICES)
    end_date = models.DateField()
    travellers = models.IntegerField(default=5)

    def __str__(self):
        return self.destination


class EmailAddress(models.Model):
    email_all = models.EmailField(unique=True)

    def __str__(self):
        return self.email_all


class TravellersGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=True, blank=True)
    travel_is = models.OneToOneField(
        Travel, on_delete=models.PROTECT, related_name="travel_group"
    )
    users = models.ManyToManyField(User, related_name="travel_group_person")

    # def save(self, *args, **kwargs):
    #     if not self.group_name:
    #         self.group_name = f"Group for {self.travel_is.name}"
    #     super().save(*args, **kwargs)


class UserRate(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="user_rate"
    )
    rate = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )


class TravelRate(models.Model):
    r_travel = models.OneToOneField(
        Travel, on_delete=models.PROTECT, related_name="travel_rate"
    )
    travel_rate = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )
