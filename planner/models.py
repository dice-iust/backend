from django.db import models
from django.conf import settings
from Travels.models import Travel

User = settings.AUTH_USER_MODEL

class Expense(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name="expenses")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name="shared_expenses")
    is_settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def split_amount(self):
        return self.amount / self.participants.count()

class Settlement(models.Model):
    payer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="payer_settlements")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="receiver_settlements")
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name="settlements")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
