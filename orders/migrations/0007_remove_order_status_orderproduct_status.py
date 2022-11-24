# Generated by Django 4.1.2 on 2022-11-05 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_orderproduct_user_alter_orderproduct_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('Placed', 'Placed'), ('Accepted', 'Accepted'), ('Shiped', 'Shiped'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Placed', max_length=20),
        ),
    ]
