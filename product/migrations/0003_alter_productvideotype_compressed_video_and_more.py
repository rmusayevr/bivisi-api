# Generated by Django 5.0.7 on 2024-09-21 12:39

import services.uploader
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvideotype',
            name='compressed_video',
            field=models.FileField(blank=True, max_length=2000, null=True, upload_to=services.uploader.Uploader.product_compress_video, verbose_name='Compressed Video (480p)'),
        ),
        migrations.AlterField(
            model_name='productvideotype',
            name='cover_image',
            field=models.ImageField(blank=True, max_length=2000, null=True, upload_to=services.uploader.Uploader.product_cover_image, verbose_name='Cover Image'),
        ),
        migrations.AlterField(
            model_name='productvideotype',
            name='original_video',
            field=models.FileField(max_length=2000, upload_to=services.uploader.Uploader.product_original_video, verbose_name='Original Video'),
        ),
    ]
