from django.shortcuts import render
from .models import Testimonial


def index(request):
    testimonials = Testimonial.objects.all()
    return render(request, "testimonials/index.html", {"testimonials": testimonials})
