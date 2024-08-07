# Generated by Django 5.0.7 on 2024-08-07 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('history', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userhistory',
            name='product_video_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_video_type', to='product.productvideotype', verbose_name='Product Video Type'),
        ),
    ]
