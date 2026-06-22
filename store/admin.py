from django.contrib import admin
from .models import Category, SubCategory, SubSubCategory, Product

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

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)