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
        "Accommodation": "/static/icons/accommodation.png",
        "Entertainment": "/static/icons/Entertainment.png",
        "Groceries": "/static/icons/Groceries.png",
        "Healthcare": "/static/icons/Healthcare.png",
        "Insurance": "/static/icons/Insurance.png",
        "Rent & Charges": "/static/icons/Rent.png",
        "Restaurants & Bars": "/static/icons/Restaurant.png",
        "Shopping": "/static/icons/Shopping.png",
        "Transport": "/static/icons/Transport.png",
        "Other": "/static/icons/Other.png",

    }

    travel = models.ForeignKey(TravellersGroup, on_delete=models.CASCADE, related_name="expenses", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2 , null=True)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payer_expenses",null=True)
    participants = models.ManyToManyField(User, related_name="participant_expenses")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Other", null=True)
    is_settled = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100, default="payment", null=True)
    description = models.TextField(null=True)
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True,default="/pay.jpg")

    @property
    def category_icon(self):
        return self.CATEGORY_ICONS.get(self.category, "default_icon.png")


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
        TravellersGroup, on_delete=models.CASCADE, related_name="settlements", null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

