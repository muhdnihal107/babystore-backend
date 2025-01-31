# Generated by Django 5.1.4 on 2025-01-19 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('orders', '0010_alter_order_cartitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cartItems',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to='cart.cartitems'),
        ),
    ]
