# Generated by Django 5.0 on 2023-12-17 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine_masters', '0017_alter_users_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
    ]
