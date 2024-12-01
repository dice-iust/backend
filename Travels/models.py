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
    name = models.CharField(max_length=200,unique=True)
    start_date = models.DateField()
    photo = models.ImageField(upload_to="profiles", default="profiles/paize2_abK6hhZ.jpg")
    destination = models.CharField(max_length=200)
    mode = models.CharField(max_length=200, choices=TYPE_CHOICES)
    start_place = models.CharField(max_length=200)
    transportation = models.CharField(max_length=200, choices=TRANS_CHOICES)
    end_date = models.DateField()
    travellers = models.IntegerField(default=5)
    empty_travellers=models.IntegerField(default=1)
    rate=models.IntegerField(default=0)
    rated_by=models.IntegerField(default=0)
    rated_by_user = models.ManyToManyField(User, related_name="rated_by_user_travel", blank=True)
    def __str__(self):
        return self.destination


class EmailAddress(models.Model):
    email_all = models.EmailField(unique=True)

    def __str__(self):
        return self.email_all


class TravellersGroup(models.Model):
    travel_is = models.OneToOneField(
        Travel, on_delete=models.PROTECT, related_name="travel_group"
    )
    users = models.ManyToManyField(User, related_name="travel_group_person")


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class UserRate(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="user_rate"
    )  
    rated_by = models.ManyToManyField(User, related_name="rated_by_user", blank=True)
    number_rated_by=models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.user} rated by {self.rated_by} - {self.user.rate}"
