from django.conf import settings
from .models import SiteContent, ListItem


def site_content(request):
    return {
        "site_content": SiteContent.load(),
        "home_facts": ListItem.objects.filter(section="home_fact"),
        "achievements": ListItem.objects.filter(section="achievement"),
        "repertoire": ListItem.objects.filter(section="repertoire"),
        "site_url": settings.SITE_URL,
        "canonical_url": settings.SITE_URL.rstrip("/") + request.path,
    }
