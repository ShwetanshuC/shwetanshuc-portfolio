from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Item, Brand, Category, ItemType


def index(request):
    items = Item.objects.filter(is_active=True, is_sold=False).select_related("brand", "category")

    brand_slug = request.GET.get("brand", "")
    category_slug = request.GET.get("category", "")
    item_type_id = request.GET.get("type", "")
    condition = request.GET.get("condition", "")

    if brand_slug:
        items = items.filter(brand__slug=brand_slug)
    if category_slug:
        items = items.filter(category__slug=category_slug)
    if item_type_id:
        try:
            items = items.filter(item_type_id=int(item_type_id))
        except (ValueError, TypeError):
            pass
    if condition:
        items = items.filter(condition=condition)

    paginator = Paginator(items, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "items": page_obj,
        "brands": Brand.objects.filter(is_active=True),
        "categories": Category.objects.filter(is_active=True),
        "item_types": ItemType.objects.filter(is_active=True).select_related("category"),
        "condition_choices": Item.CONDITION_CHOICES,
        "current_brand": brand_slug,
        "current_category": category_slug,
        "current_type": item_type_id,
        "current_condition": condition,
    }
    return render(request, "catalog/index.html", context)


def detail(request, slug):
    item = get_object_or_404(Item, slug=slug, is_active=True)
    related_items = []
    if item.category:
        related_items = (
            Item.objects.filter(category=item.category, is_active=True, is_sold=False)
            .exclude(pk=item.pk)[:4]
        )
    context = {
        "item": item,
        "related_items": related_items,
    }
    return render(request, "catalog/detail.html", context)


def by_category(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    items = Item.objects.filter(category=category, is_active=True, is_sold=False)
    paginator = Paginator(items, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "category": category,
        "page_obj": page_obj,
        "items": page_obj,
    }
    return render(request, "catalog/index.html", context)
