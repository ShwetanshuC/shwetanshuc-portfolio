from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from apps.portfolio.sitemaps import StaticViewSitemap, ProjectSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
}

ROBOTS_TXT = f"""User-agent: *
Allow: /
Disallow: /admin/

Sitemap: {settings.SITE_URL}/sitemap.xml
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", lambda r: HttpResponse(ROBOTS_TXT, content_type="text/plain")),
    path("", include("apps.portfolio.urls")),
    path("healthz/", lambda r: HttpResponse("ok")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
