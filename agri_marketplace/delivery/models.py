
from django.db import models
from django.contrib.auth.models import User

class DeliveryDetails(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Debit', 'Debit Card'),
        ('MM', 'Mobile Money'),
        ('PayPal', 'PayPal'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Delivery Details"
