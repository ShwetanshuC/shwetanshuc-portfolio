from django.contrib import admin
from django.shortcuts import redirect
from .models import Project, ProjectImage, BeforeAfterSite, SiteContent, ListItem


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # is_featured isn't shown here — nothing on the site actually reads it
    # (the projects list is ordered, not curated), so surfacing it in the
    # admin would just be a control that looks like it does something and
    # doesn't. sort_order is the one thing that actually governs display order.
    list_display = ["title", "category", "year", "sort_order"]
    list_editable = ["sort_order"]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["category"]
    inlines = [ProjectImageInline]
    fieldsets = [
        (None, {"fields": ["title", "slug", "category", "year", "short_description", "long_description"]}),
        ("Media & Links", {"fields": ["thumbnail", "live_url", "github_url", "paper_file"]}),
        ("Display", {"fields": ["tech_stack", "sort_order"]}),
    ]


@admin.register(BeforeAfterSite)
class BeforeAfterSiteAdmin(admin.ModelAdmin):
    list_display = ["title", "client_name", "has_before_url", "has_after_url", "sort_order"]
    list_editable = ["sort_order"]
    fieldsets = [
        (None, {"fields": ["title", "client_name", "tagline", "description", "sort_order"]}),
        ("Labels", {
            "fields": [("before_label", "before_year"), ("after_label", "after_year")],
            "description": "Year is optional — shown next to the label, e.g. \"Before · 2009\".",
        }),
        ("Static Screenshots", {
            "fields": ["before_screenshot", "after_screenshot"],
            "description": "Upload screenshots as a fallback when no live URLs are set.",
        }),
        ("Live Site URLs (iframe embed)", {
            "fields": ["before_url", "after_url", "visit_url"],
            "description": "If set, the before/after slider will embed live websites in an iframe instead of showing screenshots. "
                           "For Wayback Machine: use the if_ variant, e.g. https://web.archive.org/web/20200101if_/http://example.com. "
                           "visit_url adds a clickable \"Visit live site\" link when the after side is a static screenshot instead of a live iframe.",
        }),
    ]

    @admin.display(boolean=True, description="Before URL")
    def has_before_url(self, obj):
        return bool(obj.before_url)

    @admin.display(boolean=True, description="After URL")
    def has_after_url(self, obj):
        return bool(obj.after_url)


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    """Singleton — always edit the one row. List view redirects straight to it."""

    fieldsets = [
        ("Home Page", {"fields": ["home_hero_name", "home_about_eyebrow", "home_about_heading", "home_cta_heading"]}),
        ("Web Development Page", {"fields": [
            "webdev_hero_eyebrow", "webdev_hero_title", "webdev_hero_tagline",
            "webdev_response_caption", "webdev_cta_heading", "webdev_cta_text",
        ]}),
        ("Music Page", {"fields": [
            "music_intro", "music_achievements_eyebrow", "music_achievements_heading",
            "music_acoustics_text", "music_cta_heading", "music_cta_text",
        ]}),
        ("Projects Page", {"fields": ["projects_hero_title", "projects_hero_subtitle", "projects_cta_heading"]}),
        ("Before / After Page", {"fields": ["ba_hero_title", "ba_hero_subtitle"]}),
        ("Contact Page", {"fields": ["contact_hero_title", "contact_intro"]}),
    ]

    def has_add_permission(self, request):
        return not SiteContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteContent.load()
        return redirect("admin:portfolio_sitecontent_change", obj.pk)


@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    list_display = ["section", "title", "subtitle", "sort_order"]
    list_editable = ["sort_order"]
    list_filter = ["section"]
    ordering = ["section", "sort_order"]
