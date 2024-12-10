from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from products.models import Product
from cart.models import Cart, CartItem  
from .models import Order, OrderItem # Keep the import for Order and OrderItem
from django.contrib import messages
from delivery.models import DeliveryDetails

@login_required(login_url='/users/login/')
def place_order(request, delivery_id):
    # Retrieve the user's cart
    cart = Cart.objects.filter(user=request.user).first()

    # Check if the cart exists and has items
    if not cart or not cart.cart_items.exists():
        messages.error(request, "Your cart is empty. Add items before placing an order.")
        return redirect('cart_detail')

    # Retrieve delivery details by ID
    delivery_details = get_object_or_404(DeliveryDetails, id=delivery_id, user=request.user)

    # Calculate total price
    total_price = sum(item.product.price * item.quantity for item in cart.cart_items.all())

    # Create the order
    order = Order.objects.create(
        user=request.user,
        delivery_details=delivery_details,
        total_price=total_price,
        status="Pending",  # Assuming you have a status field in the Order model
    )

    # Create OrderItems for each cart item
    for item in cart.cart_items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            total_price=item.product.price * item.quantity,
        )

    # Clear the cart after placing the order
    cart.cart_items.all().delete()  # Clear all items in the cart

    # Redirect to an order confirmation page
    messages.success(request, f"Order #{order.id} has been placed successfully.")
    return redirect('order_confirmation', order_id=order.id)



def order_detail(request, order_id):
    # Use 'user' instead of 'customer'
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})



def order_success(request, order_id):
    # Retrieve the specific order by its ID
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})



@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f"Order {order.id} has been cancelled successfully.")
    else:
        messages.error(request, "This order cannot be cancelled.")

    return redirect('farmer_dashboard')

