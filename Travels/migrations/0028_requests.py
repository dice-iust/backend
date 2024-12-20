# Generated by Django 5.1.4 on 2024-12-10 16:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travels', '0027_alter_traveluserratemoney_rate_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('travel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travel_request', to='Travels.travel')),
                ('user_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
