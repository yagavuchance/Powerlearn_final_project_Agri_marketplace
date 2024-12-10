from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import supplier_required
from .forms import ProductForm
from django.core.paginator import Paginator




@login_required
@supplier_required
def supplier_dashboard(request):
    # Assuming you are filtering based on the supplier's products
    supplier_products = Product.objects.filter(supplier=request.user)
    orders = Order.objects.filter(order_items__product__in=supplier_products)
    
    context = {
        'orders': orders,
        'products': supplier_products,
    }
    return render(request, 'suppliers/supplier_dashboard.html', context)

# Add product view
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = request.user  # Set the supplier to the logged-in user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('supplier_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    return render(request, 'suppliers/add_product.html', {'form': form})

# Edit product view
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, supplier=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('supplier_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'suppliers/edit_product.html', {'form': form})

# Delete product view
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, supplier=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('supplier_dashboard')
    return render(request, 'suppliers/delete_product.html', {'product': product})

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in ["Shipped", "Delivered"]:
            order.status = status
            order.save()
            # Add a success message
            messages.success(request, f"Order #{order.id} has been marked as {status}.")

    return redirect("supplier_dashboard") 
