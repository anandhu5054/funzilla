# Generated by Django 4.1.2 on 2022-10-12 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_remove_sub_category_category'),
        ('store', '0005_remove_product_sub_category_product_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sub_Category',
        ),
    ]
