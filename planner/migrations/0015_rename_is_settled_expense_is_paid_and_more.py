# Generated by Django 5.1.4 on 2024-12-18 19:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0014_merge_20241218_1134'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='is_settled',
            new_name='is_paid',
        ),
        migrations.AddField(
            model_name='expense',
            name='participants',
            field=models.ManyToManyField(related_name='participant_expenses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='expense',
            name='receipt_image',
            field=models.ImageField(blank=True, default='/pay.jpg', null=True, upload_to='receipts/'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='title',
            field=models.CharField(default='payment', max_length=100, null=True),
        ),
    ]
