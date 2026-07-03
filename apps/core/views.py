from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    from .models import HeroSlide, FeaturedBrand, HomeSectionCard, FAQ
    context = {}
    try:
        context["hero_slides"] = list(HeroSlide.objects.filter(is_active=True).order_by("sort_order"))
    except Exception:
        context["hero_slides"] = []
    try:
        context["featured_brands"] = list(FeaturedBrand.objects.filter(is_active=True).order_by("sort_order"))
    except Exception:
        context["featured_brands"] = []
    try:
        context["section_cards"] = list(HomeSectionCard.objects.filter(is_active=True).order_by("sort_order"))
    except Exception:
        context["section_cards"] = []
    try:
        from apps.testimonials.models import Testimonial
        context["featured_testimonials"] = list(Testimonial.objects.filter(is_featured=True)[:3])
    except Exception:
        context["featured_testimonials"] = []
    try:
        from django.utils import timezone
        from apps.events.models import Event
        context["upcoming_events"] = list(
            Event.objects.filter(date__gte=timezone.now().date(), is_active=True).order_by("date")[:3]
        )
    except Exception:
        context["upcoming_events"] = []
    try:
        from apps.promotions.models import Promotion
        context["active_promotions"] = list(
            Promotion.objects.filter(is_active=True).order_by("sort_order")[:3]
        )
    except Exception:
        context["active_promotions"] = []
    return render(request, "core/home.html", context)


def about(request):
    context = {}
    try:
        from .models import FAQ
        context["faqs"] = list(FAQ.objects.filter(is_active=True).order_by("sort_order"))
    except Exception:
        context["faqs"] = []
    try:
        from apps.team.models import TeamMember
        context["team_members"] = list(TeamMember.objects.filter(is_active=True).order_by("sort_order"))
    except Exception:
        context["team_members"] = []
    return render(request, "core/about.html", context)


def handler404(request, exception=None):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
