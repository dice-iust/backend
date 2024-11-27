# Generated by Django 5.0.7 on 2024-11-27 14:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travels', '0012_alter_travel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelrate',
            name='travel_rate',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='userrate',
            name='rate',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]