from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def store(request):
    # Fetch all available products from the database
    products = Product.objects.filter(is_available=True)
    product_count = products.count()
    categories = Category.objects.all()
    context = {
        'products': products,
        'product_count': product_count,
        'categories': categories,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)