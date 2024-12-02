# Generated by Django 5.0.7 on 2024-12-02 10:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travels', '0021_travel_rated_by_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='travel',
            name='status',
            field=models.CharField(choices=[('Private', 'Private'), ('Public', 'Public')], default='Private', max_length=200),
        ),
        migrations.AlterField(
            model_name='travel',
            name='photo',
            field=models.ImageField(default='profiles/paize2_abK6hhZ.jpg', upload_to='profiles'),
        ),
        migrations.CreateModel(
            name='TravelUserRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=0, help_text='Rate between 1 and 5')),
                ('rated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_given', to=settings.AUTH_USER_MODEL)),
                ('travel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ratings', to='Travels.travel')),
                ('user_rated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]