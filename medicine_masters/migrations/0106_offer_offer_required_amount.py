# Generated by Django 5.0.1 on 2024-03-17 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine_masters', '0105_users_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='offer_required_amount',
            field=models.IntegerField(null=True),
        ),
    ]
