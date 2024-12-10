# cart/utils.py
from cart.models import Cart
from django.conf import settings
from cart.models import Cart, CartItem

def get_or_create_cart(request):
    if request.user.is_authenticated:
        # Get the cart for authenticated users
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Use session key for anonymous cart
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Create a session if it doesn't exist
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def merge_carts(session_cart, user_cart):
    for session_item in session_cart.cart_items.all():
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=session_item.product
        )
        if not created:
            user_item.quantity += session_item.quantity
            user_item.save()
    session_cart.delete()  # Remove the session cart after merging
