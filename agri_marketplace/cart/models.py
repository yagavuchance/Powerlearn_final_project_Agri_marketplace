from django.conf import settings
from django.db import models
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(Product, through='CartItem')

    def total_price(self):
        return sum(item.quantity * item.product.price for item in self.cart_items.all())

    def __str__(self):
        return f"Cart ({self.user.username})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"