# Generated by Django 5.0 on 2023-12-30 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine_masters', '0033_rename_product_origin_product_product_madein'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_advantage',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='product',
            name='product_disadvantage',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
