# Generated by Django 5.0.7 on 2024-12-03 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0009_alter_user_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rate',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
