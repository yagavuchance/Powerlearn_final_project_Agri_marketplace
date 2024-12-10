from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from orders.models import Order
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.utils import  merge_carts
from cart.models import Cart, CartItem

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()

            # Create or update the Profile model with 'is_supplier'
            is_supplier = request.POST.get('is_supplier', 'off') == 'on'
            profile, created = Profile.objects.get_or_create(user=user)
            profile.is_supplier = is_supplier
            profile.save()

            # Redirect to login page after successful registration
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def merge_carts(session_cart, user_cart):
    for session_item in session_cart.cart_items.all():
        # Check if the item already exists in the authenticated user's cart
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=session_item.product
        )
        if not created:
            # If it exists, add the quantities
            user_item.quantity += session_item.quantity
            user_item.save()
    session_cart.delete()  # Delete the session cart after merging

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Get the session cart before logging in
            session_cart_id = request.session.get('cart_id')
            session_cart = None
            if session_cart_id:
                session_cart = get_object_or_404(Cart, id=session_cart_id)

            login(request, user)  # Log the user in

            # Get or create the authenticated user's cart
            user_cart, created = Cart.objects.get_or_create(user=user)

            # Merge session cart into authenticated user's cart
            if session_cart:
                merge_carts(session_cart, user_cart)

            # Clear the session cart ID after merging
            request.session.pop('cart_id', None)

            # Redirect to 'next' or default to product list
            next_url = request.POST.get('next') or request.GET.get('next', 'product_list')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    next_url = request.GET.get('next', '')
    return render(request, 'users/login.html', {'form': form, 'next': next_url})

def custom_logout(request):
    logout(request)
    return redirect('product_list') 




# Farmer Dashboard View
@login_required
def farmer_dashboard(request):
    # Get all orders placed by the logged-in farmer
    orders = Order.objects.filter(user=request.user).order_by('-order_date')

    return render(request, 'users/farmer_dashboard.html', {'orders': orders})