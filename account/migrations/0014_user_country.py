# Generated by Django 4.2.7 on 2024-05-24 13:54

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_user_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]
