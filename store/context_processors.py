from .models import CartItem, Wishlist

def cart_counter(request):
    cart_count = 0
    cart_total = 0
    nav_cart_items = []
    wishlist_count = 0
    nav_wishlist_product_ids = set()

    if request.user.is_authenticated:
        # Cart
        all_items = CartItem.objects.filter(cart__user=request.user, is_active=True).order_by('-id')
        cart_count = sum(item.quantity for item in all_items)
        cart_total = sum(item.product.price * item.quantity for item in all_items)
        nav_cart_items = all_items[:4]

        # Wishlist
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlist_count = wishlist.items.count()
        nav_wishlist_product_ids = set(wishlist.items.values_list('product_id', flat=True))

    return {
        'cart_count':               cart_count,
        'cart_total':               cart_total,
        'nav_cart_items':           nav_cart_items,
        'wishlist_count':           wishlist_count,
        'nav_wishlist_product_ids': nav_wishlist_product_ids,
    }