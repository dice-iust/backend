# Generated by Django 5.1.4 on 2024-12-26 20:33

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_chatmessage_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='timestamp',
            field=models.DateTimeField(default=chat.models.iran_time),
        ),
    ]