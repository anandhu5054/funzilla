# Generated by Django 4.1.2 on 2022-10-27 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_user_remove_orderproduct_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_note',
        ),
    ]
