from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return ["home", "web_dev", "music", "projects", "before_after", "contact"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "home" else 0.8


class ProjectSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return reverse("project_detail", args=[obj.slug])
