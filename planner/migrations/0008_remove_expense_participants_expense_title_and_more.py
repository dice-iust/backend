# Generated by Django 5.0.7 on 2024-12-09 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0007_expense_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='participants',
        ),
        migrations.AddField(
            model_name='expense',
            name='title',
            field=models.CharField(default='payment', max_length=100),
        ),
        migrations.AlterField(
            model_name='expense',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='settlement',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
