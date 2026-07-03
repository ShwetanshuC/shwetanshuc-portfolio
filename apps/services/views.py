from django.shortcuts import render, get_object_or_404
from .models import Service


def index(request):
    services = Service.objects.filter(is_active=True).prefetch_related("features")
    return render(request, "services/list.html", {"services": services})


def detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    features = service.features.all()
    try:
        from apps.inquiries.forms import ServiceInquiryForm
        form = ServiceInquiryForm()
    except Exception:
        form = None
    context = {
        "service": service,
        "features": features,
        "form": form,
    }
    return render(request, "services/detail.html", context)
