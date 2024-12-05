from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import supplier_required
from .forms import ProductForm



@login_required
@supplier_required
def supplier_dashboard(request):
    # Get products created by the logged-in supplier
    products = request.user.products.all()

    # Get orders that include the supplier's products
    orders = Order.objects.filter(order_items__product__supplier=request.user)

    return render(request, 'suppliers/supplier_dashboard.html', {'products': products, 'orders': orders})

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


