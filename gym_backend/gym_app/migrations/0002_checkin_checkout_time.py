# Generated by Django 5.1.7 on 2025-03-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='checkout_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
