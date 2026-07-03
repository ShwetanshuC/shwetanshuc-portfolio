from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect
from .models import SiteSettings, SiteVisitCounter

# HeroSlide, FeaturedBrand, HomeSectionCard, FAQ are part of the reusable
# template but aren't wired into any template on this site — every page's
# content comes from apps.portfolio instead. Not registering them keeps the
# admin free of sections that don't do anything if you click into them.

# ---------------------------------------------------------------------------
# Custom AdminSite
# ---------------------------------------------------------------------------
class MasterAdminSite(admin.AdminSite):
    site_header = "Shwetanshu — Site Manager"
    site_title = "Site Manager"
    index_title = "Dashboard"
    # The custom top nav (base_site.html) already covers every section, and
    # the dashboard covers the rest — the default left sidebar just repeats
    # that same list (plus dead models), so it's turned off.
    enable_nav_sidebar = False

    def each_context(self, request):
        context = super().each_context(request)
        try:
            counter = SiteVisitCounter.objects.first()
            context["site_visit_count"] = counter.total_visits if counter else 0
        except Exception:
            context["site_visit_count"] = 0
        return context


# Replace default admin site
admin.site.__class__ = MasterAdminSite
admin.site.site_header = "Shwetanshu — Site Manager"
admin.site.site_title = "Site Manager"
admin.site.index_title = "Dashboard"


# ---------------------------------------------------------------------------
# SiteSettings admin — singleton redirect. Only the Site Alert fields are
# actually rendered anywhere on the live site (base.html's alert banner),
# so that's all that's shown here — the rest (contact info, social links)
# aren't wired into any template and would just be dead fields to fill in.
# ---------------------------------------------------------------------------
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fields = ["alert_enabled", "alert_message", "alert_color"]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, created = SiteSettings.objects.get_or_create(pk=1)
        return redirect(
            reverse("admin:core_sitesettings_change", args=[obj.pk])
        )


# ---------------------------------------------------------------------------
# SiteVisitCounter — read-only, single row
# ---------------------------------------------------------------------------
@admin.register(SiteVisitCounter)
class SiteVisitCounterAdmin(admin.ModelAdmin):
    list_display = ["total_visits", "updated_at"]
    readonly_fields = ["total_visits", "updated_at"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
