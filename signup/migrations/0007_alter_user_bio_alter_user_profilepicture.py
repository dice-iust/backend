# Generated by Django 5.0.7 on 2024-12-01 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0006_passwordresetrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(default="Hey! I'm using TripTide."),
        ),
        migrations.AlterField(
            model_name='user',
            name='profilePicture',
            field=models.ImageField(default='profile_pictures/photo_1_2024-11-22_00-36-00.jpg', upload_to='profile_pictures/'),
        ),
    ]
