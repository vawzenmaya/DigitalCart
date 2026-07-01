from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# ---------------------------------------------------------------------------
# Category hierarchy
# ---------------------------------------------------------------------------

class Category(models.Model):
    name        = models.CharField(max_length=50, unique=True)
    icon        = models.CharField(max_length=100, blank=True, default='ri-grid-line')
    slug        = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    menu_image  = models.ImageField(upload_to='photos/categories', blank=True, null=True)

    class Meta:
        verbose_name        = 'category'
        verbose_name_plural = 'categories'
        ordering            = ['name']

    def __str__(self):
        return self.name

    def get_product_count(self):
        """Returns count of available products in this category."""
        return self.primary_products.filter(is_available=True).count()


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name     = models.CharField(max_length=50)
    slug     = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'subcategories'
        ordering            = ['name']

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class SubSubCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name='subsubcategories', on_delete=models.CASCADE)
    name        = models.CharField(max_length=50)
    slug        = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'sub-subcategories'
        ordering            = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

class ProductManager(models.Manager):
    def available(self):
        return self.filter(is_available=True)

    def trending(self):
        return self.available().filter(is_trending=True).order_by('trending_order', '-modified_date')


class Product(models.Model):
    # Hierarchy
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='primary_products')
    additional_categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='extra_products',
        help_text='Hold down Ctrl (or Cmd on Mac) to select multiple.',
    )
    subcategory    = models.ForeignKey(SubCategory,    on_delete=models.SET_NULL, blank=True, null=True)
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.SET_NULL, blank=True, null=True)

    # Core Details
    name        = models.CharField(max_length=200, unique=True)
    slug        = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='photos/products')

    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price          = models.DecimalField(max_digits=10, decimal_places=2)

    # Inventory & Sales
    stock      = models.IntegerField(default=0)
    units_sold = models.IntegerField(default=0)

    # Metadata & Filters
    review_count     = models.IntegerField(default=0)
    is_free_delivery = models.BooleanField(default=False)
    is_available     = models.BooleanField(default=True)

    # Trending
    is_trending    = models.BooleanField(
        default=False,
        help_text='Check to include this product in the Trending section.',
    )
    trending_order = models.PositiveIntegerField(
        default=0,
        help_text='Controls display order in Trending (1 = first). Slots 2–8 are the small cards.',
    )

    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    class Meta:
        ordering = ['trending_order', '-created_date']

    def __str__(self):
        return self.name

    # --- Computed properties ---

    @property
    def discount_percentage(self):
        if self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def stock_percentage(self):
        """Percentage of stock SOLD — used for the stock bar width."""
        total = self.stock + self.units_sold
        if total == 0:
            return 0
        return int((self.units_sold / total) * 100)

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def is_low_stock(self):
        return 0 < self.stock <= 10

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', args=[self.category.slug, self.slug])


# ---------------------------------------------------------------------------
# TrendingSection — singleton-style config for the offer product + countdown
# ---------------------------------------------------------------------------

class TrendingSection(models.Model):
    """
    One active row controls:
      - which product gets the large 'offer' card (slot 1)
      - when that offer expires
    Keep only ONE row set to is_active=True at a time.
    """
    offer_product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offer_configs',
        help_text='The product shown in the big left card with the countdown timer.',
    )
    offer_ends_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When this offer expires. Leave blank to hide the countdown.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Only one TrendingSection should be active at a time.',
    )

    class Meta:
        verbose_name        = 'Trending Section Config'
        verbose_name_plural = 'Trending Section Config'

    def __str__(self):
        return f"Trending Config — offer: {self.offer_product} | ends: {self.offer_ends_at}"

    @property
    def offer_expired(self):
        if self.offer_ends_at is None:
            return False
        return timezone.now() >= self.offer_ends_at

    @property
    def seconds_remaining(self):
        """Returns total seconds left (≥0) for the JS countdown."""
        if self.offer_ends_at is None:
            return 0
        delta = self.offer_ends_at - timezone.now()
        return max(0, int(delta.total_seconds()))


# ---------------------------------------------------------------------------
# Product gallery & variants
# ---------------------------------------------------------------------------

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image   = models.ImageField(upload_to='photos/products/gallery')

    def __str__(self):
        return f"Gallery image for {self.product.name}"


VARIATION_CATEGORY_CHOICES = (
    ('color',   'Color'),
    ('size',    'Size'),
    ('storage', 'Storage'),
    ('ram',     'RAM'),
)


class Variation(models.Model):
    product            = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=VARIATION_CATEGORY_CHOICES)
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default=True)
    created_date       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_variation_category_display()}: {self.variation_value}"
    
# ---------------------------------------------------------------------------
# Cart & Cart Items
# ---------------------------------------------------------------------------

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"