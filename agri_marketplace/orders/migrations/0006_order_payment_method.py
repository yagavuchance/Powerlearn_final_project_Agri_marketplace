# Generated by Django 5.1.3 on 2024-12-12 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_delivery_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('COD', 'Cash on Delivery'), ('Debit', 'Debit Card'), ('MM', 'Mobile Money'), ('PayPal', 'PayPal')], default='COD', max_length=10),
        ),
    ]
