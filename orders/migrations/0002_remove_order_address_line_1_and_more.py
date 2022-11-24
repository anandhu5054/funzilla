# Generated by Django 4.1.2 on 2022-10-27 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_address'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='user',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.address'),
        ),
    ]