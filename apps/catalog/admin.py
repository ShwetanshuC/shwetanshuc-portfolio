from django.contrib import admin
from django.utils.html import format_html
from master_template.admin_utils import RowActionsMixin
from .models import Brand, Category, ItemType, Item, ItemImage


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    fields = ["image", "image_url", "alt_text", "sort_order", "image_focal_y"]
    extra = 1


class SoldItemProxy(Item):
    class Meta:
        proxy = True
        verbose_name = "Sold Item"
        verbose_name_plural = "Sold Items"


@admin.register(Item)
class ItemAdmin(RowActionsMixin, admin.ModelAdmin):
    list_display = [
        "title", "brand", "category", "condition", "display_price_admin",
        "is_active", "is_sold", "is_featured", "row_actions",
    ]
    list_editable = ["is_active", "is_sold", "is_featured"]
    list_display_links = ["title"]
    list_filter = ["condition", "is_active", "is_sold", "is_featured", "brand", "category"]
    search_fields = ["title", "description", "sku"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ItemImageInline]
    filter_horizontal = ["promotions"]
    fieldsets = (
        ("Item Details", {
            "fields": ("title", "slug", "brand", "category", "item_type", "condition", "year", "sku"),
        }),
        ("Pricing & Availability", {
            "fields": ("price", "hide_price", "is_active", "is_sold", "is_featured"),
        }),
        ("Description & Media", {
            "fields": ("short_description", "description", "video_url", "hero_image_focal_y"),
        }),
        ("Organization", {
            "fields": ("promotions",),
        }),
    )

    def display_price_admin(self, obj):
        if obj.hide_price or obj.price is None:
            return format_html('<span style="color:#888;font-style:italic">Contact for Price</span>')
        return f"${obj.price:,.2f}"
    display_price_admin.short_description = "Price"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_sold=False)


@admin.register(SoldItemProxy)
class SoldItemAdmin(admin.ModelAdmin):
    list_display = ["title", "brand", "category", "condition", "is_active"]
    list_filter = ["brand", "category", "condition"]
    search_fields = ["title", "sku"]

    def get_queryset(self, request):
        return Item.objects.filter(is_sold=True)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["sort_order", "name", "is_active", "website_url"]
    list_editable = ["sort_order", "is_active"]
    list_display_links = ["name"]
    ordering = ["sort_order", "name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["sort_order", "name", "is_active"]
    list_editable = ["sort_order", "is_active"]
    list_display_links = ["name"]
    ordering = ["sort_order", "name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["category", "is_active"]
