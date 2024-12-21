from django.db import models
from django.conf import settings
from Travels.models import TravellersGroup, Travel

User = settings.AUTH_USER_MODEL


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("Accommodation", "Accommodation"),
        ("Entertainment", "Entertainment"),
        ("Groceries", "Groceries"),
        ("Healthcare", "Healthcare"),
        ("Insurance", "Insurance"),
        ("Rent & Charges", "Rent & Charges"),
        ("Restaurants & Bars", "Restaurants & Bars"),
        ("Shopping", "Shopping"),
        ("Transport", "Transport"),
        ("Other", "Other"),
    ]

    CATEGORY_ICONS = {
        "Accommodation": "/media/icons/accommodation.jpg",
        "Entertainment": "/media/icons/Entertainment.jpg",
        "Groceries": "/media/icons/Groceries.jpg",
        "Healthcare": "/media/icons/Healthcare.jpg",
        "Insurance": "/media/icons/Insurance.jpg",
        "Rent & Charges": "/media/icons/Rent.jpg",
        "Restaurants & Bars": "/media/icons/Restaurant.jpg",
        "Shopping": "/media/icons/Shopping.jpg",
        "Transport": "/media/icons/Transport.jpg",
        "Other": "/media/icons/Other.jpg",
    }

    travel = models.ForeignKey(
        TravellersGroup,
        on_delete=models.CASCADE,
        related_name="expenses",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payer_expenses", null=True
    )
    participants = models.ManyToManyField(User, related_name="participant_expenses")
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="Other", null=True
    )
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100, default="payment", null=True)
    description = models.TextField(null=True)
    receipt_image = models.ImageField(upload_to="receipts/", default="/pay.jpg")
    is_paid = models.BooleanField(default=False)

    @property
    def category_icon(self):
        return self.CATEGORY_ICONS.get(self.category, "Other.jpg")

    def calculate_split(self):
        if self.participants.exists():
            return self.amount / self.participants.count()
        return 0


class Settlement(models.Model):
    payer = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="payer_settlements"
    )

    receiver = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="receiver_settlements"
    )

    travel = models.ForeignKey(
        TravellersGroup,
        on_delete=models.CASCADE,
        related_name="settlements",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)


class PastPayment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="past_payments"
    )
    expense = models.ForeignKey(
        Expense, on_delete=models.CASCADE, related_name="past_payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.expense.title} by {self.user.user_name}"
