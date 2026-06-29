from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import (
    Category, SubCategory, SubSubCategory,
    Product, ProductImage, Variation, TrendingSection,
)


# ---------------------------------------------------------------------------
# Category hierarchy
# ---------------------------------------------------------------------------

class SubSubCategoryInline(admin.TabularInline):
    model = SubSubCategory
    prepopulated_fields = {'slug': ('name',)}
    extra = 1


class SubCategoryAdmin(admin.ModelAdmin):
    list_display        = ('name', 'category')
    list_filter         = ('category',)
    search_fields       = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines             = [SubSubCategoryInline]


class SubCategoryInline(admin.TabularInline):
    model               = SubCategory
    prepopulated_fields = {'slug': ('name',)}
    extra               = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    inlines             = [SubCategoryInline]

    @admin.display(description='Products')
    def product_count(self, obj):
        return obj.primary_products.filter(is_available=True).count()


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'price', 'original_price', 'discount_badge',
        'stock', 'units_sold', 'trending_order', 'is_trending', 'is_available',
    )
    list_editable  = ('price', 'is_available', 'is_trending', 'trending_order')
    list_filter    = ('is_trending', 'is_available', 'category', 'is_free_delivery')
    search_fields  = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines             = [ProductImageInline, VariationInline]
    filter_horizontal   = ('additional_categories',)
    readonly_fields     = ('discount_badge', 'stock_percentage_display', 'created_date', 'modified_date')

    class Media:
        css = {'all': ('admin/css/product_list_fix.css',)}

    fieldsets = (
        ('Core Details', {
            'fields': ('name', 'slug', 'description', 'image', 'category', 'additional_categories', 'subcategory', 'subsubcategory'),
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'original_price', 'discount_badge', 'stock', 'units_sold', 'stock_percentage_display'),
        }),
        ('Trending Section', {
            'fields': ('is_trending', 'trending_order'),
            'description': mark_safe(
                'Check <strong>is_trending</strong> to include this product in the Trending section. '
                'Set <strong>trending_order</strong> to control the slot '
                '(1 = big offer card, 2–8 = small cards).'
            ),
        }),
        ('Metadata', {
            'fields': ('review_count', 'is_free_delivery', 'is_available', 'created_date', 'modified_date'),
        }),
    )

    @admin.display(description='Discount')
    def discount_badge(self, obj):
        pct = obj.discount_percentage
        if pct:
            return format_html('<strong style="color:#e03;">{}%</strong>', pct)
        return '—'

    @admin.display(description='Stock sold %')
    def stock_percentage_display(self, obj):
        return f"{obj.stock_percentage}%"


# ---------------------------------------------------------------------------
# TrendingSection config
# ---------------------------------------------------------------------------

@admin.register(TrendingSection)
class TrendingSectionAdmin(admin.ModelAdmin):
    list_display  = ('offer_product', 'offer_ends_at', 'countdown_status', 'is_active')
    list_editable = ('is_active',)
    raw_id_fields = ('offer_product',)

    fieldsets = (
        ('Offer Product', {
            'fields': ('offer_product',),
            'description': mark_safe(
                'This product appears in the large left card with the countdown timer. '
                'It should also have <strong>is_trending = True</strong> and '
                '<strong>trending_order = 1</strong>.'
            ),
        }),
        ('Offer Deadline', {
            'fields': ('offer_ends_at',),
            'description': mark_safe(
                'When the timer hits zero the offer card will show an '
                '<strong>OFFER ENDED</strong> banner and blur the product image. '
                'Leave blank to hide the countdown entirely.'
            ),
        }),
        ('Visibility', {
            'fields': ('is_active',),
            'description': mark_safe('Only <strong>one</strong> row should be active at a time.'),
        }),
    )

    @admin.display(description='Status')
    def countdown_status(self, obj):
        if not obj.offer_ends_at:
            return '—'
        if obj.offer_expired:
            return mark_safe('<span style="color:#c00;font-weight:bold;">EXPIRED</span>')
        remaining = obj.seconds_remaining
        days    = remaining // 86400
        hours   = (remaining % 86400) // 3600
        minutes = (remaining % 3600) // 60
        label = f'{days}d {hours}h remaining' if days > 0 else f'{hours}h {minutes}m remaining'
        return format_html('<span style="color:green;">{}</span>', label)


admin.site.register(SubCategory, SubCategoryAdmin)