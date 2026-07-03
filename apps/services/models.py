from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    image_focal_y = models.FloatField(default=0.5)
    icon_name = models.CharField(
        max_length=50, blank=True, help_text="CSS icon class or emoji"
    )
    price_display = models.CharField(
        max_length=100, blank=True, help_text="e.g. 'From $99' or 'Free estimate'"
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="features")
    feature = models.CharField(max_length=200)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Service Feature"
        verbose_name_plural = "Service Features"

    def __str__(self):
        return self.feature


class ServiceAppointment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="appointments")
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Service Appointment"
        verbose_name_plural = "Service Appointments"

    def __str__(self):
        return f"{self.customer_name} — {self.service.name}"
