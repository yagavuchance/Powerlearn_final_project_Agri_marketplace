from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product




def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # For authenticated users, associate the cart with the user
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # For anonymous users, use a session-based cart
        cart_id = request.session.get('cart_id')

        if not cart_id:
            # Create a new cart and save its ID in the session
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
        else:
            # Retrieve the existing cart
            cart = get_object_or_404(Cart, id=cart_id)

    # Add the product to the cart or increment its quantity
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{product.name} added to cart')  # Display success message
    return redirect('product_list')


def cart_detail(request):
    if request.user.is_authenticated:
        # Get or create a cart for the authenticated user
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Handle anonymous users with a session-based cart
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = get_object_or_404(Cart, id=cart_id)
        else:
            # If no cart exists in the session, create a new anonymous cart
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id

    # Render the cart details
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def remove_from_cart(request, product_id):
    cart = request.user.cart
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # Remove the item
    cart_item.delete()

    return redirect('cart_detail')  # Redirect back to the cart detail page


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

