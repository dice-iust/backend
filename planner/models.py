from datetime import timezone
from Travels.models import TravellersGroup
from django.contrib.auth import get_user_model
from django.db import models
users = get_user_model()
class Expense(models.Model):
    travel_is = models.ForeignKey(TravellersGroup, on_delete=models.CASCADE, related_name="expenses")
    created_by = models.ForeignKey(users, on_delete=models.PROTECT, related_name="created_expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    participants = models.ManyToManyField(users, related_name="shared_expenses")
    is_settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone)

    def split_amount(self):
        return self.amount / self.participants.count()

class Settlement(models.Model):
    payer = models.ForeignKey(users, on_delete=models.PROTECT, related_name="payer_settlements")
    receiver = models.ForeignKey(users, on_delete=models.PROTECT, related_name="receiver_settlements")
    travel_is = models.ForeignKey(TravellersGroup, on_delete=models.CASCADE, related_name="settlements")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone)
    is_paid = models.BooleanField(default=False)
