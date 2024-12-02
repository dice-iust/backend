# Generated by Django 5.0.7 on 2024-11-28 19:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travels', '0020_travel_rated_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='rated_by_user',
            field=models.ManyToManyField(blank=True, related_name='rated_by_user_travel', to=settings.AUTH_USER_MODEL),
        ),
    ]