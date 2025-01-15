# Generated by Django 5.1.3 on 2024-12-23 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0001_initial'),
        ('products', '0003_product_products_pr_name_9ff0a3_idx_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name_plural': 'subcategories'},
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='products_ca_name_693421_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['price'], name='products_pr_price_9b1a5f_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['created_at'], name='products_pr_created_52f0d7_idx'),
        ),
        migrations.AddIndex(
            model_name='subcategory',
            index=models.Index(fields=['category', 'name'], name='products_su_categor_2feb79_idx'),
        ),
    ]