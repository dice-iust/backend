# Generated by Django 5.0.7 on 2024-11-10 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0005_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10, null=True),
        ),
    ]
