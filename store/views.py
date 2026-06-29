from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, SubCategory, SubSubCategory, TrendingSection


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_trending_context():
    """Return shared trending context data used on the store page."""
    trending_products = (
        Product.objects
        .filter(is_available=True, is_trending=True)
        .order_by('trending_order', '-modified_date')[:9]
    )

    trending_config = TrendingSection.objects.filter(is_active=True).first()

    offer_product = None
    small_trending = list(trending_products)

    if trending_config and trending_config.offer_product:
        offer_product = trending_config.offer_product
        small_trending = [p for p in small_trending if p.pk != offer_product.pk]

    return {
        'trending_config': trending_config,
        'offer_product': offer_product,
        'trending_row1': small_trending[:4],
        'trending_row2': small_trending[4:8],
        'offer_seconds_remaining': trending_config.seconds_remaining if trending_config else 0,
        'offer_expired': trending_config.offer_expired if trending_config else False,
    }


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def store(request):
    categories = Category.objects.prefetch_related('subcategories__subsubcategories').all()

    # Search
    query = request.GET.get('query', '').strip()
    products = Product.objects.filter(is_available=True)
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    products = products.order_by('-created_date')
    product_count = products.count()

    # Pagination — 20 per page on store
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'product_count': product_count,
        'categories': categories,
        'query': query,
        'page_obj': page_obj,
        **_build_trending_context(),
    }
    return render(request, 'store/store.html', context)


def category(request, category_slug):
    current_category = get_object_or_404(
        Category.objects.prefetch_related('subcategories__subsubcategories'),
        slug=category_slug,
    )
    categories = Category.objects.prefetch_related('subcategories__subsubcategories').all()

    products = Product.objects.filter(
        is_available=True,
        category=current_category,
    )

    # --- Subcategory / sub-subcategory drill-down ---
    subcategory_slug = request.GET.get('sub')
    subsubcategory_slug = request.GET.get('subsub')
    active_sub = None
    active_subsub = None

    if subcategory_slug:
        active_sub = get_object_or_404(SubCategory, slug=subcategory_slug, category=current_category)
        products = products.filter(subcategory=active_sub)

        if subsubcategory_slug:
            active_subsub = get_object_or_404(SubSubCategory, slug=subsubcategory_slug, subcategory=active_sub)
            products = products.filter(subsubcategory=active_subsub)

    # --- Search within category ---
    query = request.GET.get('query', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # --- Discount filter ---
    discount_filter = request.GET.get('discount', '')
    if discount_filter == 'with':
        # Products where price < original_price
        products = products.extra(where=['price < original_price'])
    elif discount_filter == 'without':
        products = products.extra(where=['price >= original_price'])

    # --- Free delivery filter ---
    if request.GET.get('free_delivery'):
        products = products.filter(is_free_delivery=True)

    # --- Price range filter ---
    try:
        price_min = int(request.GET.get('price_min', 0))
        price_max = int(request.GET.get('price_max', 0))
        if price_min:
            products = products.filter(price__gte=price_min)
        if price_max:
            products = products.filter(price__lte=price_max)
    except (ValueError, TypeError):
        price_min = price_max = 0

    # --- Sorting ---
    SORT_MAP = {
        'newest':     '-created_date',
        'oldest':     'created_date',
        'price_asc':  'price',
        'price_desc': '-price',
        'popular':    '-units_sold',
        'discount':   '-original_price',   # proxy: high original = big discount likely
    }
    sort = request.GET.get('sort', 'newest')
    products = products.order_by(SORT_MAP.get(sort, '-created_date'))

    product_count = products.count()

    # --- Pagination ---
    per_page = request.GET.get('per_page', '12')
    try:
        per_page = int(per_page) if per_page != 'all' else product_count or 1
    except ValueError:
        per_page = 12

    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'current_category': current_category,
        'categories': categories,
        'products': page_obj,
        'product_count': product_count,
        'active_sub': active_sub,
        'active_subsub': active_subsub,
        'current_sort': sort,
        'query': query,
        'page_obj': page_obj,
        'per_page': per_page,
        'price_min': price_min,
        'price_max': price_max,
        'discount_filter': discount_filter,
    }
    return render(request, 'store/category.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('images', 'variations'),
        category__slug=category_slug,
        slug=product_slug,
    )

    related_products = (
        Product.objects
        .filter(category=product.category, is_available=True)
        .exclude(id=product.id)
        .order_by('-created_date')[:8]
    )

    # Group variations by category for the detail page UI
    variations = {}
    for v in product.variations.filter(is_active=True):
        variations.setdefault(v.variation_category, []).append(v)

    context = {
        'product': product,
        'related_products': related_products,
        'variations': variations,
    }
    return render(request, 'store/product_detail.html', context)