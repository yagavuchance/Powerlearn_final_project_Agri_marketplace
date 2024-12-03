from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from orders.models import Order
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import supplier_required

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

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect to the next page if provided, otherwise go to product list
            next_url = request.GET.get('next', 'product_list')  # Default to 'product_list'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('product_list') 

# Supplier Dashboard View
@login_required
@supplier_required
def supplier_dashboard(request):
    # Get products created by the logged-in supplier
    products = request.user.products.all()

    # Get orders for the products of the logged-in supplier
    orders = Order.objects.filter(product__supplier=request.user)

    return render(request, 'users/supplier_dashboard.html', {'products': products, 'orders': orders})

# Farmer Dashboard View
@login_required
def farmer_dashboard(request):
    # Get all orders placed by the logged-in farmer
    orders = Order.objects.filter(customer=request.user)

    return render(request, 'users/farmer_dashboard.html', {'orders': orders})