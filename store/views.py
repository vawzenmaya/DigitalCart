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
        .order_by('trending_order', '-modified_date')[:9]
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
    row2 = small_trending[4:8]

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


def category(request, category_slug):
    current_category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all()

    # Base queryset — products in this category (primary or additional)
    products = Product.objects.filter(
        is_available=True,
        category=current_category,
    ).order_by('-created_date')

    # --- Subcategory filter ---
    subcategory_slug = request.GET.get('sub')
    subsubcategory_slug = request.GET.get('subsub')
    active_sub = None
    active_subsub = None

    if subcategory_slug:
        from .models import SubCategory, SubSubCategory
        active_sub = get_object_or_404(SubCategory, slug=subcategory_slug, category=current_category)
        products = products.filter(subcategory=active_sub)

        if subsubcategory_slug:
            active_subsub = get_object_or_404(SubSubCategory, slug=subsubcategory_slug, subcategory=active_sub)
            products = products.filter(subsubcategory=active_subsub)

    # --- Sorting ---
    sort = request.GET.get('sort', 'newest')
    sort_map = {
        'newest':    '-created_date',
        'oldest':    'created_date',
        'price_asc': 'price',
        'price_desc':'-price',
        'popular':   '-units_sold',
    }
    products = products.order_by(sort_map.get(sort, '-created_date'))

    product_count = products.count()

    context = {
        'current_category': current_category,
        'categories': categories,
        'products': products,
        'product_count': product_count,
        'active_sub': active_sub,
        'active_subsub': active_subsub,
        'current_sort': sort,
    }
    return render(request, 'store/category.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id).order_by('-created_date')[:8]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)