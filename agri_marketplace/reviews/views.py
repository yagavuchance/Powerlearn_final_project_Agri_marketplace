from django.shortcuts import redirect
from .models import Review
from products.models import Product

def add_review(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        Review.objects.create(
            product=product,
            customer=request.user,
            rating=int(request.POST.get('rating')),
            comment=request.POST.get('comment'),
        )
    return redirect('product_detail', product_id=product.id)

