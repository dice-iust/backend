# Generated by Django 5.0.7 on 2024-12-03 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travels', '0025_traveluserratemoney_traveluserratesleep_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traveluserratemoney',
            name='rate',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='traveluserratesleep',
            name='rate',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
