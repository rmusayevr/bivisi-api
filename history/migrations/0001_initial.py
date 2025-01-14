# Generated by Django 5.0.7 on 2024-08-07 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('watch_date', models.DateTimeField(verbose_name='Watch date')),
            ],
            options={
                'verbose_name': 'User History',
                'verbose_name_plural': 'User History',
            },
        ),
    ]
