from django.shortcuts import render, get_object_or_404
from .models import Promotion


def index(request):
    promotions = Promotion.objects.filter(is_active=True).order_by("sort_order")
    return render(request, "promotions/list.html", {"promotions": promotions})


def detail(request, slug):
    promotion = get_object_or_404(Promotion, slug=slug, is_active=True)
    page = getattr(promotion, "page", None)
    blocks = page.blocks.all() if page else []
    cta_buttons = page.cta_buttons.all() if page else []
    context = {
        "promotion": promotion,
        "page": page,
        "blocks": blocks,
        "cta_buttons": cta_buttons,
    }
    return render(request, "promotions/detail.html", context)


def promotion_catalog(request, slug):
    promotion = get_object_or_404(Promotion, slug=slug, is_active=True)
    try:
        items = promotion.catalog_items.filter(is_active=True, is_sold=False)
    except Exception:
        items = []
    context = {
        "promotion": promotion,
        "items": items,
    }
    return render(request, "promotions/catalog.html", context)
