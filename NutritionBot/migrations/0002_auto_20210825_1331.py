# Generated by Django 3.2.6 on 2021-08-25 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NutritionBot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='bmr',
            field=models.FloatField(blank=True, default=0.0, max_length=255),
        ),
        migrations.AddField(
            model_name='user_info',
            name='water',
            field=models.FloatField(blank=True, default=0.0, max_length=255),
        ),
    ]