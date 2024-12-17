from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from orders.models import Order  # Ensure you import the Order model
from .models import Payment  # Import the Payment model


@login_required(login_url='/users/login/')
def payment_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        entered_amount = float(request.POST.get('amount', 0))

        if entered_amount == order.total_price:
            with transaction.atomic():
                # Create a Payment record
                Payment.objects.create(
                    user=request.user,
                    order=order,
                    amount_paid=entered_amount,
                    total_amount=order.total_price,
                )

                # Update order payment status to "Paid" (order status remains "Pending")
                order.payment_status = "Paid"
                order.save()

            messages.success(request, f'Payment successful! Order #{order.id} has been updated.')
            return redirect('order_confirmation', order_id=order.id)
        else:
            messages.error(request, "Entered amount does not match the order total. Please try again.")

    return render(request, 'payment/checkout.html', {'order': order})
