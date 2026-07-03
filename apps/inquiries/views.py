from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactInquiryForm, ItemInquiryForm, ServiceInquiryForm, QuoteRequestForm


def _check_honeypot(form):
    """Returns True if honeypot triggered (spam)."""
    return bool(form.data.get("website", ""))


def contact(request):
    if request.method == "POST":
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent. We will be in touch soon.")
            return redirect("inquiry_thank_you")
    else:
        form = ContactInquiryForm()
    return render(request, "inquiries/contact.html", {"form": form})


def item_inquiry(request, item_slug):
    try:
        from apps.catalog.models import Item
        item = get_object_or_404(Item, slug=item_slug, is_active=True)
    except Exception:
        item = None

    if request.method == "POST":
        form = ItemInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.item = item
            inquiry.save()
            messages.success(request, "Thank you! We have received your inquiry and will contact you shortly.")
            return redirect("inquiry_thank_you")
    else:
        form = ItemInquiryForm()
    return render(request, "inquiries/contact.html", {"form": form, "item": item})


def service_inquiry(request, service_slug):
    try:
        from apps.services.models import Service
        service = get_object_or_404(Service, slug=service_slug, is_active=True)
    except Exception:
        service = None

    if request.method == "POST":
        form = ServiceInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.service = service
            inquiry.save()
            messages.success(request, "Thank you! Your service inquiry has been received.")
            return redirect("inquiry_thank_you")
    else:
        form = ServiceInquiryForm()
    return render(request, "inquiries/contact.html", {"form": form, "service": service})


def quote_request(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your quote request has been submitted. We will review it and get back to you.")
            return redirect("inquiry_thank_you")
    else:
        form = QuoteRequestForm()
    return render(request, "inquiries/contact.html", {"form": form, "is_quote": True})


def thank_you(request):
    return render(request, "inquiries/thank_you.html")
