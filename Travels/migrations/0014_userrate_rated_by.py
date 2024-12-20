# Generated by Django 5.0.7 on 2024-11-27 14:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travels', '0013_alter_travelrate_travel_rate_alter_userrate_rate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userrate',
            name='rated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rated_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
