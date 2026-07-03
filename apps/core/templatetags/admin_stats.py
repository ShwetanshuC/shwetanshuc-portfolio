from django import template
from django.db.utils import OperationalError, ProgrammingError

register = template.Library()


@register.simple_tag
def site_stats():
    try:
        from apps.core.models import SiteVisitCounter
        from apps.portfolio.models import Project
        from apps.inquiries.models import ContactInquiry
        from apps.testimonials.models import Testimonial

        project_count = Project.objects.count()

        try:
            unread = ContactInquiry.objects.filter(is_read=False).count()
        except (OperationalError, ProgrammingError):
            unread = 0

        try:
            visitor_total = (
                SiteVisitCounter.objects
                .filter(pk=1)
                .values_list("total_visits", flat=True)
                .first() or 0
            )
        except (OperationalError, ProgrammingError):
            visitor_total = 0

        testimonial_count = Testimonial.objects.count()

        return {
            "projects": project_count,
            "inbox_unread": unread,
            "visitors": visitor_total,
            "testimonials": testimonial_count,
        }
    except Exception:
        return {
            "projects": 0,
            "inbox_unread": 0,
            "visitors": 0,
            "testimonials": 0,
        }
