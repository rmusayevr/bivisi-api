# Generated by Django 4.2.7 on 2024-06-12 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='product link'),
        ),
    ]
