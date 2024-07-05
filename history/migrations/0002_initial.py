# Generated by Django 4.2.7 on 2024-07-04 09:43

from django.db import migrations, models
import django.db.models.deletion


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
