# Generated by Django 4.2.7 on 2024-05-27 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('watch_date', models.DateTimeField(verbose_name='Watch date')),
                ('product_video_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_video_type', to='product.productvideotype', verbose_name='Product Video Type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_history', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User History',
                'verbose_name_plural': 'User History',
                'indexes': [models.Index(fields=['user', 'product_video_type'], name='history_use_user_id_e598a2_idx')],
                'unique_together': {('user', 'product_video_type')},
            },
        ),
    ]