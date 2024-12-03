from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product

@login_required
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{product.name} added to cart')  # Display success message
    return redirect('product_list')  # Redirect to cart details page

@login_required
def cart_detail(request):
    cart_items = request.user.cart.cart_items.all()  # Adjust this query as per your structure
    for item in cart_items:
        item.total_price = item.quantity * item.product.price

    context = {
        'cart': request.user.cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart_detail.html', context)

def remove_from_cart(request, product_id):
    cart = request.user.cart
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # Remove the item
    cart_item.delete()

    return redirect('cart_detail')  # Redirect back to the cart detail page

@login_required
def update_quantity(request, product_id):
    cart = request.user.cart
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    quantity = request.POST.get('quantity')
    if quantity:
        quantity = int(quantity)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()

    return redirect('cart_detail')  # Redirect back to the cart detail page

