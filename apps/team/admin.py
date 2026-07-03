from django.contrib import admin
from django.utils.html import format_html
from .models import Department, TeamMember


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["sort_order", "name"]
    list_editable = ["sort_order"]
    list_display_links = ["name"]
    ordering = ["sort_order", "name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["photo_thumbnail", "name", "role", "department", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    list_display_links = ["name"]
    list_filter = ["department", "is_active"]
    search_fields = ["name", "role", "bio"]
    ordering = ["sort_order", "name"]

    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:50%">',
                obj.photo.url,
            )
        return format_html('<span style="color:#ccc">No photo</span>')
    photo_thumbnail.short_description = "Photo"
