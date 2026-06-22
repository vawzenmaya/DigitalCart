from django.contrib import admin
from .models import Category, SubCategory, SubSubCategory, Product, ProductImage, Variation

# 1. The inline for Sub-SubCategories
class SubSubCategoryInline(admin.TabularInline):
    model = SubSubCategory
    prepopulated_fields = {'slug': ('name',)}
    extra = 1

# 2. Register SubCategory to show the Sub-SubCategory inline
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubSubCategoryInline]

# 3. The inline for SubCategories
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    prepopulated_fields = {'slug': ('name',)}
    extra = 1

# 4. Register the main Category
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    inlines = [SubCategoryInline]

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'original_price', 'stock', 'units_sold', 'category', 'is_trending', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_available', 'is_trending') # Allows you to check/uncheck trending directly from the list view!
    inlines = [ProductImageInline, VariationInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)