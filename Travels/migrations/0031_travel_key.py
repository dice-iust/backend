# Generated by Django 5.1.4 on 2024-12-11 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travels', '0030_requests_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='key',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
