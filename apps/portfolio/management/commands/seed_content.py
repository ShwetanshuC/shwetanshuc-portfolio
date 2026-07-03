from django.core.management.base import BaseCommand

from apps.portfolio.models import Project, BeforeAfterSite


PROJECTS = [
    dict(
        title="Southern Park Music School",
        slug="southern-park-music-school",
        category="marketing",
        short_description="Full production website for a local music school — events, blog, gallery, and inquiry forms.",
        long_description=(
            "Complete Django rebuild of a long-established music school's web presence: "
            "event management, a student blog, a photo gallery, lesson inquiry forms, and a "
            "content-manageable admin so staff can update it without touching code."
        ),
        tech_stack="Django, Python, AWS, Docker, CI/CD",
        live_url="https://southernparkmusicschool.com",
        is_featured=True,
        sort_order=1,
        year=2024,
    ),
    dict(
        title="Miller Piano Showroom",
        slug="miller-piano-showroom",
        category="cms",
        short_description="Piano inventory catalog with brand/condition filtering, events, and a staff-editable admin.",
        long_description=(
            "Inventory catalog for a piano retailer — brand and condition filtering, event "
            "listings, testimonials, promotions, and a clean admin panel built for non-technical staff."
        ),
        tech_stack="Django, PostgreSQL, Railway",
        is_featured=True,
        sort_order=2,
        year=2024,
    ),
    dict(
        title="DockChain",
        slug="dockchain",
        category="research",
        short_description="IoT-based port security and check-in platform, built at UNC Wilmington's SIPS Lab.",
        long_description=(
            "A Django platform combining license-plate recognition and fingerprint verification "
            "into a single port check-in step, aimed at cutting truck wait times at maritime ports. "
            "Built as a team of four during NCSSM Summer Ventures (1 of 38 students selected "
            "statewide), using Arduino hardware for the physical gate and a three-tier web app for "
            "logistics coordination. I served as primary author and presented at the Summer "
            "Ventures Networking Symposium; abstract accepted to the Scopus/Web of Science–indexed "
            "International Conference on Cyber Warfare & Security."
        ),
        tech_stack="Django, Python, Arduino, OpenAI API, MySQL",
        is_featured=True,
        sort_order=3,
        year=2025,
    ),
    dict(
        title="Violin Shoppe",
        slug="violin-shoppe",
        category="marketing",
        short_description="Boutique violin shop site with instrument catalog, repair services, and teacher bios.",
        long_description=(
            "Instrument catalog, repair-service booking, teacher bios, an event calendar, and "
            "online inquiry forms for repairs and rentals."
        ),
        tech_stack="Django, CSS, JavaScript",
        sort_order=4,
        year=2025,
    ),
    dict(
        title="Case Brothers",
        slug="case-brothers",
        category="web_app",
        short_description="Internal operations site with inventory tracking, blog, and events for a local business.",
        long_description=(
            "Internal business site with inventory tracking, event listings, a blog, and a "
            "services module for day-to-day operations."
        ),
        tech_stack="Django, Python",
        sort_order=5,
        year=2025,
    ),
    dict(
        title="Southern Park Acoustics",
        slug="southern-park-acoustics",
        category="craft",
        short_description="Ongoing acoustic treatment of a recital hall, built by hand as a thank-you to my teacher.",
        long_description=(
            "The recital hall where I trained had muddy, unclear acoustics. As a thank-you to my "
            "teacher, Dr. Michael Lehtinen, Kieran Lee and I are designing and installing internal "
            "Rockwool acoustic treatment for the full hall — learning the acoustics math, "
            "consulting with professionals, and building and placing the panels ourselves. "
            "Still in progress."
        ),
        tech_stack="Rockwool, Acoustic Modeling, Woodworking",
        sort_order=6,
        year=2025,
    ),
]


class Command(BaseCommand):
    help = "Seed real Project and BeforeAfterSite records for the portfolio site."

    def handle(self, *args, **options):
        for data in PROJECTS:
            obj, created = Project.objects.update_or_create(
                slug=data["slug"], defaults=data
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} project: {obj.title}")

        ba, created = BeforeAfterSite.objects.update_or_create(
            title="Southern Park Music School",
            defaults=dict(
                client_name="Southern Park Music School",
                tagline="Static HTML to full Django + AWS build",
                description="Replaced a static, hard-to-update site with a CMS the school's own staff can maintain.",
                after_url="https://southernparkmusicschool.com",
                before_label="Before",
                after_label="After",
                sort_order=1,
            ),
        )
        self.stdout.write(f"{'Created' if created else 'Updated'} before/after: {ba.title}")

        self.stdout.write(self.style.SUCCESS("Portfolio content seeded."))
