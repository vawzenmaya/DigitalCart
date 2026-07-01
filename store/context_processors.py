from .models import CartItem

def cart_counter(request):
    cart_count = 0
    cart_total = 0
    nav_cart_items = []
    
    if request.user.is_authenticated:
        # Fetch items, ordering by newest first
        all_items = CartItem.objects.filter(cart__user=request.user, is_active=True).order_by('-id')
        cart_count = sum(item.quantity for item in all_items)
        cart_total = sum(item.product.price * item.quantity for item in all_items)
        nav_cart_items = all_items[:4] # Grab just the first 4 for the mini-cart
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
        'nav_cart_items': nav_cart_items
    }