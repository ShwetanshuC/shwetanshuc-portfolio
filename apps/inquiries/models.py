from django.db import models


class BaseInquiry(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"


class ContactInquiry(BaseInquiry):
    subject = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ["-submitted_at"]


class ProjectInquiry(BaseInquiry):
    business_name = models.CharField(max_length=200, blank=True)
    budget_range = models.CharField(max_length=100, blank=True)
    project_type = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Project Inquiry"
        verbose_name_plural = "Project Inquiries"
        ordering = ["-submitted_at"]
