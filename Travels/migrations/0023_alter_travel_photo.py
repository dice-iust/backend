# Generated by Django 5.0.7 on 2024-12-02 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travels', '0022_travel_description_travel_status_alter_travel_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='photo',
            field=models.ImageField(blank=True, default='profiles/paize.jpg', upload_to='profiles'),
        ),
    ]
