from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.utils import timezone
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
    list_display = ('name', 'category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubSubCategoryInline]


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    prepopulated_fields = {'slug': ('name',)}
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    inlines = [SubCategoryInline]


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
        'name', 'price', 'original_price', 'discount_badge',
        'stock', 'units_sold', 'category',
        'trending_order', 'is_trending', 'is_available',
    )
    list_editable = ('price', 'is_available', 'is_trending', 'trending_order')
    list_filter = ('is_trending', 'is_available', 'category')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, VariationInline]

    # Give the name column much more room via custom CSS injected into the page
    class Media:
        css = {
            'all': ('admin/css/product_list_fix.css',)
        }

    fieldsets = (
        ('Core Details', {
            'fields': ('name', 'slug', 'description', 'image', 'category', 'subcategory', 'subsubcategory'),
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'original_price', 'stock', 'units_sold'),
        }),
        ('Trending Section', {
            'fields': ('is_trending', 'trending_order'),
            'description': mark_safe(
                'Check <strong>is_trending</strong> to include this product in the Trending section. '
                'Set <strong>trending_order</strong> to control the slot '
                '(1 = big offer card, 2 to 8 = small cards). '
                'Only the first 8 trending products (by order) are shown.'
            ),
        }),
        ('Metadata', {
            'fields': ('review_count', 'is_free_delivery', 'is_available'),
        }),
    )

    @admin.display(description='Discount')
    def discount_badge(self, obj):
        pct = obj.discount_percentage
        if pct:
            return format_html('<span style="color:#e03;">{}</span>', str(pct) + '%')
        return '—'


# ---------------------------------------------------------------------------
# TrendingSection config
# ---------------------------------------------------------------------------
@admin.register(TrendingSection)
class TrendingSectionAdmin(admin.ModelAdmin):
    list_display = ('offer_product', 'offer_ends_at', 'countdown_status', 'is_active')
    list_editable = ('is_active',)
    # Use raw_id_fields instead of autocomplete_fields to avoid any FK-related
    # format_html issues in Django 6.
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
                '<strong>OFFER ENDED</strong> diagonal banner and blur the product image. '
                'Leave blank to hide the countdown entirely.'
            ),
        }),
        ('Active', {
            'fields': ('is_active',),
            'description': mark_safe(
                'Only <strong>one</strong> Trending Section Config should be '
                'active at a time.'
            ),
        }),
    )

    @admin.display(description='Status')
    def countdown_status(self, obj):
        """Safe status column — never passes None or unformatted values to format_html."""
        if not obj.offer_ends_at:
            return '—'
        if obj.offer_expired:
            return mark_safe('<span style="color:#c00;font-weight:bold;">EXPIRED</span>')
        remaining = obj.seconds_remaining
        days    = remaining // 86400
        hours   = (remaining % 86400) // 3600
        minutes = (remaining % 3600) // 60

        if days > 0:
            label = '%dd %dh remaining' % (days, hours)
        else:
            label = '%dh %dm remaining' % (hours, minutes)

        return format_html(
            '<span style="color:green;">{}</span>',
            label,
        )


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)