from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product
from categories.models import Category
from reviews.models import Review

def product_list(request):
    # Fetch query parameters
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    sort_option = request.GET.get('sort', '')
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    page_number = request.GET.get('page', 1)

    # Base queryset
    products = Product.objects.all()

    # Filter by category
    if category_id:
        products = products.filter(category_id=category_id)

    # Search functionality
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Filter by price range
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sort functionality
    if sort_option == 'name':
        products = products.order_by('name')
    elif sort_option == 'price':
        products = products.order_by('price')
    elif sort_option == 'stock':
        products = products.order_by('stock')

    # Pagination
    paginator = Paginator(products, 9)  # Show 9 products per page
    products = paginator.get_page(page_number)

    # Fetch all categories
    categories = Category.objects.all()

    # Pass context to the template
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_id': category_id,
        'sort_option': sort_option,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, product_id):
    # Fetch product and related reviews
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews})
