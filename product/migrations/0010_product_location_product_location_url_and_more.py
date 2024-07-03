# Generated by Django 4.2.7 on 2024-07-02 12:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_productpropertyandvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='product',
            name='location_url',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator()], verbose_name='Location URL'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_link',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='product link'),
        ),
    ]
