from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project, BeforeAfterSite


def home(request):
    return render(request, "portfolio/home.html")


def music(request):
    return render(request, "portfolio/music.html")


def web_dev(request):
    try:
        from apps.testimonials.models import Testimonial
        testimonials = list(Testimonial.objects.filter(is_featured=True)[:6])
    except Exception:
        testimonials = []

    ba_sites = list(BeforeAfterSite.objects.all()[:3])
    context = {
        "testimonials": testimonials,
        "ba_sites": ba_sites,
    }
    return render(request, "portfolio/web_dev.html", context)


def projects(request):
    context = {"projects": list(Project.objects.all())}
    return render(request, "portfolio/projects.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "portfolio/project_detail.html", {"project": project})


def before_after(request):
    sites = list(BeforeAfterSite.objects.all())
    return render(request, "portfolio/before_after.html", {"sites": sites})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        honeypot = request.POST.get("website", "")

        if honeypot:
            return redirect("contact_success")

        if name and email and message:
            try:
                from apps.inquiries.models import ContactInquiry
                ContactInquiry.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message,
                )
            except Exception:
                pass
            return redirect("contact_success")
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, "portfolio/contact.html")


def contact_success(request):
    return render(request, "portfolio/contact_success.html")
