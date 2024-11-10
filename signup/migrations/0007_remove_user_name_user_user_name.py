# Generated by Django 5.0.7 on 2024-11-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0006_alter_user_birth_date_alter_user_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(default='yourname', max_length=100, unique=True),
        ),
    ]