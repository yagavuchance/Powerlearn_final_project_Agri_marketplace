from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from products.models import Product
from cart.models import Cart, CartItem  
from .models import Order, OrderItem # Keep the import for Order and OrderItem


@login_required(login_url='/users/login/')
def place_order(request):
    # Fetch the user's cart
    cart = Cart.objects.get(user=request.user)
    if not cart.cart_items.exists():
        return redirect('cart_detail')  # Redirect if the cart is empty

    # Initialize the total price for the order
    total_price = 0

    # Calculate total price for all cart items
    for item in cart.cart_items.all():
        total_price += item.product.price * item.quantity

    # Create the order (without product/quantity)
    order = Order.objects.create(
        customer=request.user,  # Use the logged-in user as the customer
        total_price=total_price,  # Store the total price
        status='Pending'
    )

    # Create OrderItems for each cart item
    for item in cart.cart_items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            total_price=item.product.price * item.quantity,  # Calculate total price for this item
        )

    # Optionally, clear the cart after placing the order
    cart.cart_items.all().delete()

    # Redirect to an order confirmation page
    return redirect('order_confirmation', order_id=order.id)  # Ensure this URL exists



def order_success(request, order_id):
    # Retrieve the specific order by its ID
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required(login_url='/users/login/')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})

