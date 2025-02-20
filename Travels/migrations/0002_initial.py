# Generated by Django 5.1.4 on 2024-12-22 19:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Travels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='user_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='travel',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='admin_trips', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='travel',
            name='rated_by_user',
            field=models.ManyToManyField(blank=True, related_name='rated_by_user_travel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requests',
            name='travel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travel_request', to='Travels.travel'),
        ),
        migrations.AddField(
            model_name='travellersgroup',
            name='travel_is',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='travel_group', to='Travels.travel'),
        ),
        migrations.AddField(
            model_name='travellersgroup',
            name='users',
            field=models.ManyToManyField(related_name='travel_group_person', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='traveluserratemoney',
            name='rated_by',
            field=models.ManyToManyField(related_name='ratings_given_money', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='traveluserratemoney',
            name='travel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ratings_money', to='Travels.travel'),
        ),
        migrations.AddField(
            model_name='traveluserratemoney',
            name='user_rated',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_received_money', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='traveluserratesleep',
            name='rated_by',
            field=models.ManyToManyField(related_name='ratings_given_sleep', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='traveluserratesleep',
            name='travel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ratings_sleep', to='Travels.travel'),
        ),
        migrations.AddField(
            model_name='traveluserratesleep',
            name='user_rated',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_received_sleep', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userrate',
            name='rated_by',
            field=models.ManyToManyField(blank=True, related_name='rated_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userrate',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='user_rate', to=settings.AUTH_USER_MODEL),
        ),
    ]
