# Generated by Django 4.2.7 on 2024-07-30 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_productvideotype_product_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='like_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Like Count'),
        ),
        migrations.AddIndex(
            model_name='productcomment',
            index=models.Index(fields=['user', 'product'], name='product_pro_user_id_bd6a1f_idx'),
        ),
        migrations.AddIndex(
            model_name='productcommentlike',
            index=models.Index(fields=['user'], name='product_pro_user_id_02bbfe_idx'),
        ),
        migrations.AddIndex(
            model_name='productpropertyandvalue',
            index=models.Index(fields=['product'], name='product_pro_product_73bc62_idx'),
        ),
        migrations.AddIndex(
            model_name='userproductlike',
            index=models.Index(fields=['user'], name='product_use_user_id_660ad1_idx'),
        ),
    ]