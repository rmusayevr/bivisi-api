# Generated by Django 5.0.7 on 2024-08-07 10:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('history', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_history', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddIndex(
            model_name='userhistory',
            index=models.Index(fields=['user', 'product_video_type'], name='history_use_user_id_e598a2_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='userhistory',
            unique_together={('user', 'product_video_type')},
        ),
    ]
