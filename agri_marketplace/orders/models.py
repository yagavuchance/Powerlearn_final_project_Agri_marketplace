from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from delivery.models import DeliveryDetails

class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Canceled", "Canceled"),
    ]

    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Debit', 'Debit Card'),
        ('MM', 'Mobile Money'),
        ('PayPal', 'PayPal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_details = models.ForeignKey(DeliveryDetails, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')  
    payment_status = models.CharField(max_length=20, default='Pending')  
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, null=True, blank=True)  
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username if self.user else 'Unknown User'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"
