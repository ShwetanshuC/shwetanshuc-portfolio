import uuid
from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    logo = models.ImageField(upload_to="catalog/brands/", blank=True, null=True)
    website_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="catalog/categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ItemType(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="item_types"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Item Type"
        verbose_name_plural = "Item Types"

    def __str__(self):
        return f"{self.category.name} — {self.name}"


class Item(models.Model):
    CONDITION_NEW = "new"
    CONDITION_USED = "used"
    CONDITION_REFURBISHED = "refurbished"
    CONDITION_CHOICES = [
        (CONDITION_NEW, "New"),
        (CONDITION_USED, "Pre-Owned"),
        (CONDITION_REFURBISHED, "Refurbished"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    brand = models.ForeignKey(
        Brand, null=True, blank=True, on_delete=models.SET_NULL, related_name="items"
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="items"
    )
    item_type = models.ForeignKey(
        ItemType, null=True, blank=True, on_delete=models.SET_NULL, related_name="items"
    )
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default=CONDITION_NEW)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hide_price = models.BooleanField(
        default=False, help_text="Show 'Contact for Price' instead of the price"
    )
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    sku = models.CharField(max_length=100, blank=True, null=True, unique=True)
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo embed URL")
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    hero_image_focal_y = models.FloatField(default=0.5)
    promotions = models.ManyToManyField(
        "promotions.Promotion",
        blank=True,
        related_name="catalog_items",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            if Item.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def display_price(self):
        if self.hide_price or self.price is None:
            return "Contact for Price"
        return f"${self.price:,.2f}"

    @property
    def primary_image(self):
        return self.images.first()


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="catalog/items/", blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="Alternative: link to external image")
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    image_focal_y = models.FloatField(default=0.5)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Item Image"
        verbose_name_plural = "Item Images"

    def __str__(self):
        return f"Image for {self.item.title} (#{self.sort_order})"
