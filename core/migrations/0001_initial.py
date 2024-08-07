# Generated by Django 5.0.7 on 2024-08-07 10:23

import services.uploader
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('faq', models.CharField(max_length=300, unique=True, verbose_name='faq')),
                ('answer', models.CharField(max_length=300, verbose_name='answer')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQ',
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('image', models.ImageField(max_length=500, upload_to=services.uploader.Uploader.slider_image, verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Slider',
                'verbose_name_plural': 'Sliders',
            },
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('room_id', models.CharField(max_length=100, unique=True, verbose_name='room id')),
                ('room_name', models.CharField(max_length=255, verbose_name='room name')),
                ('user_name', models.CharField(max_length=255, verbose_name='user name')),
                ('cover_image', models.ImageField(max_length=500, upload_to=services.uploader.Uploader.stream_image, verbose_name='cover image')),
            ],
            options={
                'verbose_name': 'Stream',
                'verbose_name_plural': 'Streams',
            },
        ),
    ]
