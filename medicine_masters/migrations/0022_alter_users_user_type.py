# Generated by Django 5.0 on 2023-12-24 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine_masters', '0021_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_type',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=2),
        ),
    ]
