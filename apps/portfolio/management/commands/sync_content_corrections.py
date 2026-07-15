from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from apps.portfolio.models import BeforeAfterSite, ListItem, Project, SiteContent

FINANCE_FACT = "Interned in financial automation at Integrus Partners — EBITDA modeling, M&A screening."

ACOUSTICS_TEXT = (
    "A thank-you to my teacher, Dr. Michael Lehtinen: Kieran Lee and I are building "
    "and installing Rockwool acoustic treatment for the recital hall where I trained. "
    "Still in progress."
)

CONTACT_INTRO = (
    "Whether it's a new website, a redesign, a custom web application, or a piano "
    "accompaniment or performance opportunity — I'd love to hear about it. I work "
    "directly with clients, no middlemen."
)

PROJECT_DESCRIPTIONS = {
    "southern-park-music-school": (
        "Rebuilt a 60-year-old music school's web presence as a full Django CMS: "
        "staff-editable events, faculty pages, gallery, and honeypot-protected inquiry forms "
        "feeding a Django admin the office actually uses. Deployed on AWS (S3, Docker, GitHub "
        "Actions CI/CD) with structured-data markup and a Search Console submission that took "
        "the site to a #1 Google Places ranking for local searches within a few months."
    ),
    "miller-piano-showroom": (
        "Inventory catalog for a piano retailer, replacing a static WordPress site the staff "
        "couldn't update. Items are fully admin-managed — no code changes to list a new piano — "
        "with server-rendered filtering (brand, condition, type) for speed and indexability. "
        "Includes events, testimonials, and promotions modules. PostgreSQL, deployed on Railway "
        "with automatic deploys from main."
    ),
    "dockchain": (
        "Automates manual port check-in by pairing license-plate recognition with fingerprint "
        "verification at an Arduino-driven gate: a camera reads the plate, a sensor confirms the "
        "driver, and the barrier opens only on a matched, pre-registered pairing. The web layer "
        "is a three-tier Django system — driver/company registration, an operator dashboard for "
        "logs, and a hardware bridge writing check-in events to MySQL over serial. Built as a "
        "team of four during NCSSM Summer Ventures (1 of 38 selected statewide) — I served as "
        "primary author, studying the maritime industry to define the problem, with teammates "
        "building out hardware and interface. Presented at the Summer Ventures Symposium; "
        "abstract later accepted to the Scopus/Web of Science–indexed International Conference "
        "on Cyber Warfare & Security."
    ),
    "southern-park-acoustics": (
        "The recital hall where I trained had a live, boomy sound — hard walls and a low ceiling "
        "caused slap echo and poor clarity near the back rows. Kieran Lee and I are treating it "
        "with hand-built Rockwool mineral-wool panels (pine frame, acoustically transparent "
        "fabric wrap), placed at first-reflection points derived from the hall's architectural "
        "floorplan for the most audible improvement per panel. We modeled the room's actual "
        "non-rectangular geometry in AmRoc Pro, a finite-element room mode solver, to find its "
        "low-frequency resonant modes and Schroeder frequency (~117 Hz) — confirming the panels "
        "solve mid/high-frequency clarity, while true bass control (thicker absorbers, corner "
        "bass traps) remains future work. Still installing — a thank-you to my teacher, "
        "Dr. Michael Lehtinen."
    ),
    "pokemon-card-pricing": (
        "Photograph a Pokémon card, get its identity and live market price back. Detection uses "
        "classical CV (Canny edge detection into a perspective warp, HSV fallback, 4-rotation "
        "auto-orient) before a two-tier identification pipeline: a vision-language model (Gemini, "
        "or a local Ollama model offline) reads name/set/HP directly, falling back to EasyOCR on "
        "a normalized crop when foil glare breaks confidence. A locally fine-tuned EfficientNet "
        "embedder catches what OCR misses — glare, off-angle shots, foil distortion — by matching "
        "against known card embeddings. Matches are priced via the Pokémon TCG API, with the "
        "result page showing the raw OCR read for debuggability. Still training and testing "
        "locally, not yet deployed."
    ),
}


class Command(BaseCommand):
    """One-off content corrections applied against an already-seeded production
    database, where the normal fixture reseed (which only fires on an empty
    database) won't pick up later copy edits. Every check here is idempotent —
    safe to run on every boot."""

    help = "Applies content corrections/additions that predate the current seed fixture."

    def handle(self, *args, **options):
        content = SiteContent.objects.first()
        if content and "Royal Conservatory" in content.music_intro:
            content.music_intro = (
                "Started at seven. Ten years of classical piano — "
                "Bach, Chopin, Mozart, Beethoven, Schubert. Still playing."
            )
            content.save(update_fields=["music_intro"])
            self.stdout.write("Fixed SiteContent.music_intro")

        if content and content.music_acoustics_text != ACOUSTICS_TEXT:
            content.music_acoustics_text = ACOUSTICS_TEXT
            content.save(update_fields=["music_acoustics_text"])
            self.stdout.write("Fixed SiteContent.music_acoustics_text")

        if content and content.contact_intro != CONTACT_INTRO:
            content.contact_intro = CONTACT_INTRO
            content.save(update_fields=["contact_intro"])
            self.stdout.write("Fixed SiteContent.contact_intro")

        for item in ListItem.objects.filter(section="home_fact"):
            if "RCM" in item.title or "Royal Conservatory" in item.title:
                item.title = "Classical piano since age seven."
                item.save(update_fields=["title"])
                self.stdout.write(f"Fixed ListItem #{item.pk}")

        if not ListItem.objects.filter(section="home_fact", title=FINANCE_FACT).exists():
            last_order = ListItem.objects.filter(section="home_fact").count()
            ListItem.objects.create(section="home_fact", title=FINANCE_FACT, sort_order=last_order)
            self.stdout.write("Added Integrus Partners home_fact")

        for slug, description in PROJECT_DESCRIPTIONS.items():
            updated = Project.objects.filter(slug=slug).exclude(long_description=description).update(
                long_description=description
            )
            if updated:
                self.stdout.write(f"Tightened long_description for {slug}")

        # DockChain's Before/After card postdates the original seed fixture
        # (which only has Miller Piano and Southern Park) — added here rather
        # than to the fixture itself, since the fixture only loads once on an
        # empty database and this production DB is long past that point.
        # No visit_url on purpose: DockChain isn't hosted anywhere public yet,
        # so the "Visit live site" button stays hidden until it is.
        dockchain_ba, created = BeforeAfterSite.objects.update_or_create(
            title="DockChain",
            defaults=dict(
                tagline="Built by Shwetanshu Chakraborthy, Aadarsh Jena, Leon Baiye & Taizhe Zhu",
                after_label="Prototype",
                sort_order=3,
            ),
        )
        if created:
            self.stdout.write("Created DockChain before/after entry")
        if not dockchain_ba.after_screenshot:
            image_path = Path(__file__).resolve().parents[4] / "static" / "images" / "dockchain-site-home.jpg"
            if image_path.exists():
                with open(image_path, "rb") as f:
                    dockchain_ba.after_screenshot.save("dockchain-site-home.jpg", File(f), save=True)
                self.stdout.write("Uploaded DockChain after_screenshot")
