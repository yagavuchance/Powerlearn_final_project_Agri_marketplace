from django.db import models
from django.contrib.auth.models import User
from orders.models import Order  # Import the correct Order model

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)  # Correct reference to the Order model
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user} - Amount Paid: {self.amount_paid}"
