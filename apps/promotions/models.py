from django.db import models
from django.urls import reverse
from colorfield.fields import ColorField


class Promotion(models.Model):
    TEMPLATE_HERO = "hero"
    TEMPLATE_SPOTLIGHT = "spotlight"
    TEMPLATE_CARD = "card"
    TEMPLATE_RIBBON = "ribbon"
    TEMPLATE_IMAGE_BANNER = "image_banner"
    TEMPLATE_CHOICES = [
        (TEMPLATE_HERO, "Hero"),
        (TEMPLATE_SPOTLIGHT, "Spotlight"),
        (TEMPLATE_CARD, "Card"),
        (TEMPLATE_RIBBON, "Ribbon"),
        (TEMPLATE_IMAGE_BANNER, "Image Banner"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default=TEMPLATE_HERO)
    is_active = models.BooleanField(default=True)
    is_featured_home = models.BooleanField(
        default=False, help_text="Show on home page"
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("promotion_detail", args=[self.slug])


class PromotionPage(models.Model):
    promotion = models.OneToOneField(
        Promotion, on_delete=models.CASCADE, related_name="page"
    )
    hero_image = models.ImageField(upload_to="promotions/hero/", blank=True, null=True)
    hero_image_focal_y = models.FloatField(default=0.5)
    mobile_image = models.ImageField(upload_to="promotions/mobile/", blank=True, null=True)
    mobile_image_focal_y = models.FloatField(default=0.5)
    image_no_crop = models.BooleanField(default=False)
    bg_color = ColorField(default="#1a1a1a")
    heading = models.CharField(max_length=200, blank=True)
    subheading = models.CharField(max_length=300, blank=True)
    body_text = models.TextField(blank=True)
    cta_url = models.URLField(blank=True)
    cta_label = models.CharField(max_length=80, blank=True, default="Shop Now")

    class Meta:
        verbose_name = "Promotion Page"
        verbose_name_plural = "Promotion Pages"

    def __str__(self):
        return f"Page for {self.promotion.title}"


class PromotionBlock(models.Model):
    BLOCK_TEXT = "text"
    BLOCK_IMAGE = "image"
    BLOCK_HEADING = "heading"
    BLOCK_DIVIDER = "divider"
    BLOCK_SPACER = "spacer"
    BLOCK_CHOICES = [
        (BLOCK_TEXT, "Text"),
        (BLOCK_IMAGE, "Image"),
        (BLOCK_HEADING, "Heading"),
        (BLOCK_DIVIDER, "Divider"),
        (BLOCK_SPACER, "Spacer"),
    ]

    page = models.ForeignKey(
        PromotionPage, on_delete=models.CASCADE, related_name="blocks"
    )
    block_type = models.CharField(max_length=20, choices=BLOCK_CHOICES)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="promotions/blocks/", blank=True, null=True)
    image_focal_y = models.FloatField(default=0.5)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Promotion Block"
        verbose_name_plural = "Promotion Blocks"

    def __str__(self):
        return f"{self.get_block_type_display()} block #{self.sort_order}"


class PromotionCTA(models.Model):
    STYLE_PRIMARY = "primary"
    STYLE_SECONDARY = "secondary"
    STYLE_OUTLINE = "outline"
    STYLE_CHOICES = [
        (STYLE_PRIMARY, "Primary"),
        (STYLE_SECONDARY, "Secondary"),
        (STYLE_OUTLINE, "Outline"),
    ]

    page = models.ForeignKey(
        PromotionPage, on_delete=models.CASCADE, related_name="cta_buttons"
    )
    label = models.CharField(max_length=80)
    url = models.URLField()
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default=STYLE_PRIMARY)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Promotion CTA"
        verbose_name_plural = "Promotion CTAs"

    def __str__(self):
        return self.label
