from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def store(request):
    # Fetch all categories for the mega menu
    categories = Category.objects.all()
    
    # Fetch ALL available products
    products = Product.objects.filter(is_available=True).order_by('-created_date')
    
    # Fetch ONLY the trending products (you check this box in the admin)
    trending_products = Product.objects.filter(is_available=True, is_trending=True).order_by('-modified_date')
    
    product_count = products.count()
    
    context = {
        'products': products,
        'trending_products': trending_products,
        'categories': categories,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)