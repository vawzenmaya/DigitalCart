from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, ExpressionWrapper, F, BooleanField
from .models import Product, Category, SubCategory, SubSubCategory, TrendingSection
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Variation


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

    # --- Discount filter (pure ORM — no raw SQL) ---
    discount_filter = request.GET.get('discount', '')
    if discount_filter == 'with':
        products = products.filter(price__lt=F('original_price'))
    elif discount_filter == 'without':
        products = products.filter(price__gte=F('original_price'))

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
        'discount':   '-original_price',
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

    # These are needed by the shared dpt-cat header partial
    categories = Category.objects.prefetch_related('subcategories__subsubcategories').all()

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
        'categories': categories,
        'product_count': Product.objects.filter(is_available=True).count(),
    }
    return render(request, 'store/product_detail.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('store')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to DigitalCart, {user.username}! Your account has been created.")
            next_url = request.GET.get('next', 'store')
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'store')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('store')

# ---------------------------------------------------------------------------
# Cart Views
# ---------------------------------------------------------------------------

@login_required(login_url='login')
def cart(request):
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_obj, is_active=True).order_by('id')
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)
    
    # Flat shipping fee placeholder as per your HTML
    shipping = 10000 
    grand_total = total + shipping if total > 0 else 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    product_variations = []

    if request.method == 'POST':
        # Grab quantity from the form, default to 1
        qty = int(request.POST.get('quantity', 1))
        
        # Loop through POST data to find matching variations
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product, 
                    variation_category__iexact=key, 
                    variation_value__iexact=value
                )
                product_variations.append(variation)
            except Variation.DoesNotExist:
                pass
    else:
        qty = 1

    # Check if this exact product with these exact variations is already in the cart
    cart_items = CartItem.objects.filter(product=product, cart=cart_obj)
    
    if cart_items.exists():
        existing_var_lists = []
        id_list = []
        for item in cart_items:
            existing_variations = list(item.variations.all())
            existing_var_lists.append(existing_variations)
            id_list.append(item.id)

        if product_variations in existing_var_lists:
            # Increase quantity of the existing exact match
            index = existing_var_lists.index(product_variations)
            item_id = id_list[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += qty
            item.save()
        else:
            # Create a new cart item for the new variation
            item = CartItem.objects.create(product=product, quantity=qty, cart=cart_obj)
            if product_variations:
                item.variations.add(*product_variations)
            item.save()
    else:
        # Product not in cart at all, create new
        cart_item = CartItem.objects.create(product=product, quantity=qty, cart=cart_obj)
        if product_variations:
            cart_item.variations.add(*product_variations)
        cart_item.save()

    return redirect('cart')

@login_required(login_url='login')
def remove_cart_item(request, item_id):
    """Decreases quantity by 1. Removes item if quantity reaches 0."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def delete_cart_item(request, item_id):
    """Completely deletes the item regardless of quantity."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

def about(request):
    return render(request, 'store/about.html')

# ---------------------------------------------------------------------------
# Wishlist views
# ---------------------------------------------------------------------------
from .models import Wishlist, WishlistItem
from django.views.decorators.http import require_POST
from django.http import JsonResponse


@login_required(login_url='login')
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items      = wishlist.items.select_related('product').all()
    categories = Category.objects.prefetch_related('subcategories__subsubcategories').all()
    context = {
        'wishlist_items': items,
        'wishlist_count': wishlist.items.count(),
        'categories':     categories,
    }
    return render(request, 'store/wishlist.html', context)


@login_required(login_url='login')
@require_POST
def wishlist_toggle(request, product_id):
    """AJAX: adds if absent, removes if present. Always returns JSON."""
    product  = get_object_or_404(Product, pk=product_id, is_available=True)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()

    if item:
        item.delete()
        added = False
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        added = True

    return JsonResponse({
        'ok':      True,
        'added':   added,
        'count':   wishlist.items.count(),
        'message': 'Added to Wishlist' if added else 'Removed from Wishlist',
    })


@login_required(login_url='login')
@require_POST
def wishlist_remove(request, item_id):
    """Direct remove used by the wishlist page itself."""
    item = get_object_or_404(WishlistItem, pk=item_id, wishlist__user=request.user)
    item.delete()
    wishlist = Wishlist.objects.get(user=request.user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'count': wishlist.items.count()})

    return redirect('wishlist')