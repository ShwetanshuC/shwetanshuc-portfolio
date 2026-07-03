from django.contrib import admin
from .models import Promotion, PromotionPage, PromotionBlock, PromotionCTA


class PromotionBlockInline(admin.StackedInline):
    model = PromotionBlock
    fields = ["block_type", "content", "image", "image_focal_y", "sort_order"]
    extra = 0

    class Media:
        js = ["https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"]


class PromotionCTAInline(admin.TabularInline):
    model = PromotionCTA
    fields = ["label", "url", "style", "sort_order"]
    extra = 0


class PromotionPageInline(admin.StackedInline):
    model = PromotionPage
    fields = [
        "hero_image", "hero_image_focal_y",
        "mobile_image", "mobile_image_focal_y",
        "image_no_crop", "bg_color",
        "heading", "subheading", "body_text",
        "cta_url", "cta_label",
    ]
    extra = 1
    max_num = 1


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        "title", "template", "is_active", "is_featured_home",
        "start_date", "end_date", "sort_order",
    ]
    list_editable = ["is_active", "is_featured_home", "sort_order"]
    list_display_links = ["title"]
    list_filter = ["template", "is_active", "is_featured_home"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PromotionPageInline]
