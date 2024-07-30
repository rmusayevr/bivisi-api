# Generated by Django 4.2.7 on 2024-07-30 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='basket',
            index=models.Index(fields=['user', 'is_active'], name='order_baske_user_id_3651a7_idx'),
        ),
        migrations.AddIndex(
            model_name='basketitem',
            index=models.Index(fields=['user', 'product'], name='order_baske_user_id_9033ef_idx'),
        ),
        migrations.AddIndex(
            model_name='favorite',
            index=models.Index(fields=['user'], name='order_favor_user_id_f6ada4_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user', 'basket'], name='order_order_user_id_ed43ec_idx'),
        ),
    ]
