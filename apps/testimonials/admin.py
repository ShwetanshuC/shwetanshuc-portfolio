from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["author_name", "rating", "is_featured", "source", "date", "created_at"]
    list_editable = ["is_featured"]
    list_display_links = ["author_name"]
    list_filter = ["rating", "is_featured", "source"]
    search_fields = ["author_name", "content"]
