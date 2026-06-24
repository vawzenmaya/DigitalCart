from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=100, blank=True, default='ri-grid-line')
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    menu_image = models.ImageField(upload_to='photos/categories', blank=True, null=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.name


class SubSubCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name='subsubcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'sub-subcategories'

    def __str__(self):
        return self.name


class Product(models.Model):
    # Hierarchy
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.CASCADE, blank=True, null=True)

    # Core Details
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/products')

    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Inventory & Sales
    stock = models.IntegerField()
    units_sold = models.IntegerField(default=0)

    # Metadata & Filters
    review_count = models.IntegerField(default=0)
    is_free_delivery = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    # --- TRENDING ---
    is_trending = models.BooleanField(
        default=False,
        help_text="Check to include this product in the Trending section."
    )
    trending_order = models.PositiveIntegerField(
        default=0,
        help_text="Controls display order in Trending (1 = first). Slots 2–8 are the small cards."
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['trending_order', '-created_date']

    @property
    def discount_percentage(self):
        if self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return int(discount)
        return 0

    @property
    def stock_percentage(self):
        """Percentage of stock SOLD — used for the stock bar width."""
        total = self.stock + self.units_sold
        if total == 0:
            return 0
        return int((self.units_sold / total) * 100)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# TrendingSection — a singleton-style config row for the offer product
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
        help_text="The product shown in the big left card with the countdown timer."
    )
    offer_ends_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this offer expires. Leave blank to hide the countdown."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Only one TrendingSection should be active at a time."
    )

    class Meta:
        verbose_name = 'Trending Section Config'
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
        """Returns total seconds left (>=0) for use in the JS countdown."""
        if self.offer_ends_at is None:
            return 0
        delta = self.offer_ends_at - timezone.now()
        return max(0, int(delta.total_seconds()))


# ---------------------------------------------------------------------------
# Product gallery & variants — unchanged
# ---------------------------------------------------------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products/gallery')

    def __str__(self):
        return f"Gallery image for {self.product.name}"


variation_category_choices = (
    ('color', 'color'),
    ('size', 'size'),
    ('storage', 'storage'),
    ('ram', 'ram'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.variation_value