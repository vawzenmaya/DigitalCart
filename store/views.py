from django.shortcuts import render, get_object_or_404
from .models import Product, Category, TrendingSection


def store(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).order_by('-created_date')
    product_count = products.count()

    # Trending: fetch 8 products ordered by trending_order
    trending_products = (
        Product.objects
        .filter(is_available=True, is_trending=True)
        .order_by('trending_order', '-modified_date')[:8]
    )

    # Active TrendingSection config
    trending_config = TrendingSection.objects.filter(is_active=True).first()

    # Separate offer product from small cards
    offer_product = None
    small_trending = list(trending_products)

    if trending_config and trending_config.offer_product:
        offer_product = trending_config.offer_product
        small_trending = [p for p in small_trending if p.pk != offer_product.pk]

    row1 = small_trending[:4]
    row2 = small_trending[4:7]

    # Compute these EAGERLY in the view so the template gets plain Python
    # primitives — avoids any timezone subtlety when properties are evaluated
    # lazily during template rendering.
    offer_seconds_remaining = trending_config.seconds_remaining if trending_config else 0
    offer_expired = trending_config.offer_expired if trending_config else False

    context = {
        'products': products,
        'product_count': product_count,
        'categories': categories,
        'trending_config': trending_config,
        'offer_product': offer_product,
        'trending_row1': row1,
        'trending_row2': row2,
        'offer_seconds_remaining': offer_seconds_remaining,
        'offer_expired': offer_expired,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)