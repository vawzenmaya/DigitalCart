from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
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

# Add this new model
class SubSubCategory(models.Model):
    # Links directly to the SubCategory above it
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
    image = models.ImageField(upload_to='photos/products') # Main display image
    
    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2) # The crossed-out price
    price = models.DecimalField(max_digits=10, decimal_places=2) # The current selling price
    
    # Inventory & Sales
    stock = models.IntegerField()
    units_sold = models.IntegerField(default=0)
    
    # Metadata & Filters
    review_count = models.IntegerField(default=0)
    is_free_delivery = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False) # Check this to show in the Trending section
    is_available = models.BooleanField(default=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Automatically calculates the percentage discount to use in the HTML
    @property
    def discount_percentage(self):
        if self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return int(discount)
        return 0

    def __str__(self):
        return self.name

# Model for Multiple Images (Gallery)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products/gallery')

    def __str__(self):
        return f"Gallery image for {self.product.name}"

# Model for dynamic variants (Color, Size, RAM, Storage)
variation_category_choices = (
    ('color', 'color'),
    ('size', 'size'),
    ('storage', 'storage'),
    ('ram', 'ram'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100) # e.g., "Red", "256GB", "XL"
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.variation_value