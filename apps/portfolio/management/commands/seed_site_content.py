from django.core.management.base import BaseCommand

from apps.portfolio.models import ListItem, SiteContent


HOME_FACTS = [
    "Classical piano since age seven. RCM-trained.",
    "Self-taught Django. Founder, Chakraborthy Web Development.",
    "UNC Kenan-Flagler, Class of 2030 — Business & Data Science.",
]

ACHIEVEMENTS = [
    dict(title="Grand Prize", subtitle="Charleston International Piano Competition"),
    dict(title="Performed at Carnegie Hall", subtitle=""),
    dict(title="Featured on NBC, CBS, FOX & AP News", subtitle=""),
    dict(title="Top prizes", subtitle="American Protégé (Piano & Strings), NC Music"),
    dict(title="Accompanied and mentored 400+ students", subtitle='to "Superior" competition rankings'),
]

REPERTOIRE = [
    dict(title="J.S. Bach", subtitle="Well-Tempered Clavier",
         detail="Where I learned that structure and beauty aren't opposites. Every voice has a purpose."),
    dict(title="Frédéric Chopin", subtitle="Nocturnes & Ballades",
         detail="The pieces that made me understand phrasing — that the space between notes matters as much as the notes."),
    dict(title="Ludwig van Beethoven", subtitle="Sonatas Op. 13, Op. 27",
         detail="Difficulty is worth it when the result is genuinely expressive."),
    dict(title="Franz Schubert", subtitle="Impromptus D. 899",
         detail="Long-form musical thinking. The kind of patience that transfers directly to building anything worthwhile."),
    dict(title="W.A. Mozart", subtitle="Piano Concertos",
         detail="Economy. Not a note wasted. The hardest aesthetic to achieve and the one I most admire."),
    dict(title="Claude Debussy", subtitle="Préludes",
         detail="Texture and atmosphere. A different way of thinking about color and time."),
]


class Command(BaseCommand):
    help = "Seed SiteContent singleton and ListItem rows (home facts, achievements, repertoire)."

    def handle(self, *args, **options):
        SiteContent.load()
        self.stdout.write("SiteContent row ready (edit at /admin/portfolio/sitecontent/).")

        ListItem.objects.filter(section="home_fact").delete()
        for i, text in enumerate(HOME_FACTS):
            ListItem.objects.create(section="home_fact", title=text, sort_order=i)

        ListItem.objects.filter(section="achievement").delete()
        for i, item in enumerate(ACHIEVEMENTS):
            ListItem.objects.create(section="achievement", sort_order=i, **item)

        ListItem.objects.filter(section="repertoire").delete()
        for i, item in enumerate(REPERTOIRE):
            ListItem.objects.create(section="repertoire", sort_order=i, **item)

        self.stdout.write(self.style.SUCCESS("Seeded home facts, achievements, and repertoire."))
