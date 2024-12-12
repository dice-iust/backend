# Generated by Django 5.1.2 on 2024-12-11 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planner", "0008_expense_title_alter_expense_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="category",
            field=models.CharField(
                choices=[
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
                ],
                default="Other",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="expense",
            name="custom_category",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
