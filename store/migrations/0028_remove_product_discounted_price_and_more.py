# Generated by Django 4.1.2 on 2022-11-09 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_product_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discounted_price',
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Discount',
        ),
    ]