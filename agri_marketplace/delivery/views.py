from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from delivery.forms import DeliveryDetailsForm
from .models import DeliveryDetails
from cart.models import Cart
from orders.models import Order, OrderItem


@login_required(login_url='/users/login/')
def checkout(request):
    if request.method == 'POST':
        form = DeliveryDetailsForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')  # Retrieve payment method

            with transaction.atomic():  # Use atomic transaction for data integrity
                # Save delivery details
                delivery_details = form.save(commit=False)
                delivery_details.user = request.user
                delivery_details.save()

                # Retrieve or create the user's cart
                cart, created = Cart.objects.get_or_create(user=request.user)

                if cart and cart.cart_items.exists():  # Ensure the cart exists and has items
                    # Calculate the total price
                    total_price = cart.total_price()

                    # Create the order
                    order = Order.objects.create(
                        user=request.user,
                        delivery_details=delivery_details,
                        payment_method=payment_method,  # Save payment method in Order
                        total_price=total_price,
                        status="Pending",
                    )

                    # Create `OrderItem` entries for each cart item
                    for cart_item in cart.cart_items.all():
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                            price=cart_item.product.price,
                            total_price=cart_item.quantity * cart_item.product.price,
                        )

                    # Clear the cart items
                    cart.cart_items.all().delete()

                    # Redirect based on payment method
                    if payment_method == 'Debit':  # Redirect to payment checkout for Debit Card
                        return redirect('payment_checkout', order_id=order.id)
                    elif payment_method == 'PayPal':
                        return redirect('payment_checkout', order_id=order.id)
                    elif payment_method == 'MM':
                        # Add logic for Mobile Money or redirect to its payment page
                        return redirect('payment_checkout', order_id=order.id)
                    elif payment_method == 'COD':
                        messages.success(request, f'Order #{order.id} placed successfully. Payment will be collected on delivery.')
                        return redirect('order_confirmation', order_id=order.id)
                else:
                    messages.error(request, 'Your cart is empty. Add items before proceeding to checkout.')
                    return redirect('cart_detail')
        else:
            messages.error(request, 'Please fix the errors in the delivery form.')
    else:
        form = DeliveryDetailsForm()

    # Retrieve the cart for display
    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(request, 'delivery/checkout.html', {'form': form, 'cart': cart})





@login_required(login_url='/users/login/')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'delivery/order_confirmation.html', {'order': order})
