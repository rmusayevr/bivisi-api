# Generated by Django 4.2.7 on 2024-05-07 13:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basket',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AddField(
            model_name='basketitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basketitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wishlist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
    ]
