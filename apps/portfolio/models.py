from django.db import models


class OOSBlurb(models.Model):
    """A social-proof blurb card for the Out-of-Style scatter section."""

    PLATFORM_CHOICES = [
        ('tweet',     'Tweet (X / Twitter)'),
        ('email',     'Email'),
        ('sms',       'SMS / iMessage'),
        ('review',    'Google Review'),
        ('yelp',      'Yelp Review'),
        ('instagram', 'Instagram'),
    ]
    SENTIMENT_CHOICES = [('bad', 'Bad (negative)'), ('good', 'Good (positive)')]
    DIRECTION_CHOICES = [('in', 'In (received)'), ('out', 'Out (sent)')]

    platform  = models.CharField(max_length=12, choices=PLATFORM_CHOICES)
    sentiment = models.CharField(max_length=4, choices=SENTIMENT_CHOICES)
    light_mode = models.BooleanField(default=False, help_text='Use light card background instead of dark')
    active     = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    live_dur   = models.FloatField(default=5.0, help_text='Post-reveal loop duration in seconds (e.g. 4.5)')
    live_delay = models.FloatField(default=0.0, help_text='Post-reveal loop start delay in seconds (e.g. 1.4)')

    # ── Tweet fields ──────────────────────────────────────────────────────────
    author_name   = models.CharField(max_length=80, blank=True)
    author_handle = models.CharField(max_length=80, blank=True, help_text='Include @, e.g. @sarah_chen')
    avatar_color  = models.CharField(max_length=20, blank=True, help_text='CSS colour, e.g. #e07060')

    # ── Email fields ──────────────────────────────────────────────────────────
    from_email = models.CharField(max_length=150, blank=True)
    subject    = models.CharField(max_length=250, blank=True)

    # ── SMS bubbles (up to 3 messages) ────────────────────────────────────────
    sms_1_dir  = models.CharField(max_length=3, choices=DIRECTION_CHOICES, blank=True)
    sms_1_text = models.CharField(max_length=200, blank=True)
    sms_2_dir  = models.CharField(max_length=3, choices=DIRECTION_CHOICES, blank=True)
    sms_2_text = models.CharField(max_length=200, blank=True)
    sms_3_dir  = models.CharField(max_length=3, choices=DIRECTION_CHOICES, blank=True)
    sms_3_text = models.CharField(max_length=200, blank=True)

    # ── Review / Yelp fields ──────────────────────────────────────────────────
    star_count     = models.PositiveSmallIntegerField(default=5, help_text='1–5 stars')
    reviewer_label = models.CharField(max_length=120, blank=True, help_text='e.g. "Google Review, 2024"')

    # ── Instagram fields ──────────────────────────────────────────────────────
    ig_username  = models.CharField(max_length=80,  blank=True, help_text='e.g. @their_business')
    ig_followers = models.CharField(max_length=40,  blank=True, help_text='Display string, e.g. 4,821 followers')
    ig_likes     = models.CharField(max_length=40,  blank=True, help_text='Display string, e.g. 847 likes')

    # ── Shared body text (tweet, email, review, yelp, instagram caption) ──────
    body_text = models.TextField(blank=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'OOS Blurb'
        verbose_name_plural = 'OOS Blurbs'

    def __str__(self):
        preview = (self.body_text or self.sms_1_text or '')[:50]
        return f'[{self.get_platform_display()}] {self.get_sentiment_display()} — {preview}'

    @property
    def stars_html(self):
        n = max(1, min(5, self.star_count))
        return '★' * n + '☆' * (5 - n)

    @property
    def css_classes(self):
        classes = f'wd-si wd-si--{self.platform} wd-si--{self.sentiment}'
        if self.light_mode:
            classes += ' wd-si--light'
        return classes

    @property
    def sms_bubbles(self):
        bubbles = []
        for i in (1, 2, 3):
            d = getattr(self, f'sms_{i}_dir')
            t = getattr(self, f'sms_{i}_text')
            if d and t:
                bubbles.append((d, t))
        return bubbles


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("web_app", "Web Application"),
        ("ecommerce", "E-Commerce"),
        ("marketing", "Marketing Site"),
        ("cms", "Custom CMS"),
        ("research", "Research & Product"),
        ("craft", "Hands-On / Craft"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="marketing")
    short_description = models.CharField(max_length=300)
    long_description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=300, help_text="Comma-separated: Django, Python, Tailwind CSS")
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    paper_file = models.FileField(
        upload_to="projects/papers/", blank=True, null=True,
        help_text="Optional PDF — e.g. a research paper or writeup related to this project."
    )
    thumbnail = models.ImageField(upload_to="projects/thumbnails/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)
    year = models.PositiveSmallIntegerField(default=2024)

    class Meta:
        ordering = ["sort_order", "-year"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    link_url = models.URLField(blank=True, help_text="Optional — makes the photo clickable, e.g. a live search result or source page.")
    related_search_queries = models.CharField(
        max_length=500, blank=True,
        help_text="Comma-separated search queries that also rank #1 for this site. "
                   "Each renders as a small chip that opens a live Google search in a new tab."
    )
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Project Photo"
        verbose_name_plural = "Project Photos"

    def __str__(self):
        return f"{self.project.title} — {self.caption or self.image.name}"

    @property
    def related_query_list(self):
        return [q.strip() for q in self.related_search_queries.split(",") if q.strip()]


class SiteContent(models.Model):
    """Singleton holding the editable copy for every major page. One row only —
    edit it in the admin instead of touching templates."""

    # --- Home ---
    home_hero_name = models.CharField(max_length=100, default="Shwetanshu")
    home_about_eyebrow = models.CharField(max_length=100, default="About me")
    home_about_heading = models.TextField(
        default="A pianist,\na developer,\nand a lot more.",
        help_text="One line per line break — rendered with line breaks preserved.",
    )
    home_cta_heading = models.CharField(max_length=200, default="Want to work together?")

    # --- Web Development page ---
    webdev_hero_eyebrow = models.CharField(
        max_length=200, default="Full-stack · Django & Python · Production deployments"
    )
    webdev_hero_title = models.CharField(max_length=200, default="Websites that work.")
    webdev_hero_tagline = models.TextField(
        default="I design, build, and host Django sites for local businesses — no page "
        "builders, no templates. Every client owns a real admin panel and a site that actually ranks."
    )
    webdev_response_caption = models.CharField(
        max_length=200, default="Shwetanshu responding to a client email, wherever he happens to be."
    )
    webdev_cta_heading = models.CharField(max_length=200, default="Ready to build something?")
    webdev_cta_text = models.CharField(
        max_length=300, default="Tell me what you need. I'll give you an honest scope and timeline."
    )

    # --- Music page ---
    music_intro = models.TextField(
        default="Started at seven. Ten years of classical piano — "
        "Bach, Chopin, Mozart, Beethoven, Schubert. Still playing."
    )
    music_achievements_eyebrow = models.CharField(max_length=100, default="Notable achievements")
    music_achievements_heading = models.CharField(max_length=200, default="On the record")
    music_acoustics_text = models.TextField(
        default="A thank-you to my teacher, Dr. Michael Lehtinen: Kieran Lee and I are building "
        "and installing Rockwool acoustic treatment for the recital hall where I trained. "
        "Still in progress."
    )
    music_cta_heading = models.CharField(max_length=200, default="Want to talk about a website?")
    music_cta_text = models.CharField(
        max_length=300, default="The music is personal. The web work is how I earn — and I take it just as seriously."
    )

    # --- Projects page ---
    projects_hero_title = models.CharField(max_length=200, default="A few things I'm excited to show")
    projects_hero_subtitle = models.CharField(
        max_length=300, default="Client sites, a research build, and a couple projects that aren't even done yet."
    )
    projects_cta_heading = models.CharField(max_length=200, default="Want a site like one of these?")

    # --- Before / After page ---
    ba_hero_title = models.CharField(max_length=200, default="Same business, new site")
    ba_hero_subtitle = models.CharField(
        max_length=300, default="Drag the slider to compare what was there before against what's live now."
    )

    # --- Contact page ---
    contact_hero_title = models.CharField(max_length=200, default="Let's Build Something Together")
    contact_intro = models.TextField(
        default="Whether it's a new website, a redesign, a custom web application, or a piano "
        "accompaniment or performance opportunity — I'd love to hear about it. I work directly "
        "with clients, no middlemen."
    )

    class Meta:
        verbose_name = "Site Content"
        verbose_name_plural = "Site Content"

    def __str__(self):
        return "Site Content (edit this)"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def home_about_heading_lines(self):
        return self.home_about_heading.splitlines()


class ListItem(models.Model):
    """Small reusable rows for repeating content blocks — quick facts, achievements,
    repertoire — so they can be added/reordered/edited from the admin."""

    SECTION_CHOICES = [
        ("home_fact", "Home — Quick Facts"),
        ("achievement", "Music — Notable Achievements"),
        ("repertoire", "Music — Repertoire & Influences"),
    ]
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    title = models.CharField(max_length=200, help_text="Fact text / achievement headline / composer name")
    subtitle = models.CharField(max_length=200, blank=True, help_text="Venue-year / piece title")
    detail = models.TextField(blank=True, help_text="Optional note or description")
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["section", "sort_order", "id"]
        verbose_name = "List Item"
        verbose_name_plural = "List Items (facts / achievements / repertoire)"

    def __str__(self):
        return f"[{self.get_section_display()}] {self.title}"


class BeforeAfterSite(models.Model):
    title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200, blank=True)
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    before_screenshot = models.ImageField(upload_to="before_after/before/", blank=True, null=True)
    after_screenshot = models.ImageField(upload_to="before_after/after/", blank=True, null=True)
    before_label = models.CharField(max_length=100, default="Before")
    after_label = models.CharField(max_length=100, default="After")
    before_year = models.CharField(max_length=20, blank=True, help_text="e.g. 2009 — shown next to the Before label")
    after_year = models.CharField(max_length=20, blank=True, help_text="e.g. 2026 — shown next to the After label")
    before_url = models.URLField(
        blank=True,
        help_text="Wayback Machine embed URL — append 'if_/' before the original URL, e.g. https://web.archive.org/web/20200101if_/http://example.com"
    )
    after_url = models.URLField(blank=True, help_text="Live URL of the new site (must allow iframe embedding)")
    visit_url = models.URLField(
        blank=True,
        help_text="Live URL to link to when the after-side is a static screenshot (not embedded as an iframe). "
                   "Makes the after panel clickable without the slow/unreliable live-iframe load."
    )
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Before/After Site"
        verbose_name_plural = "Before/After Sites"

    def __str__(self):
        return self.title
