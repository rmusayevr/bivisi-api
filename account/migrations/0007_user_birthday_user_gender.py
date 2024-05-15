# Generated by Django 4.2.7 on 2024-05-15 08:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_phonenumber_created_at_phonenumber_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='birthday'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default=1, max_length=30, verbose_name='gender'),
            preserve_default=False,
        ),
    ]
