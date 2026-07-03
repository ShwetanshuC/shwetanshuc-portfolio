from django.db import models


class Testimonial(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    author_name = models.CharField(max_length=120)
    author_title = models.CharField(max_length=120, blank=True)
    author_photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    is_featured = models.BooleanField(default=False)
    date = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=80, blank=True, help_text="e.g. Google, Yelp, direct")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.author_name} — {self.rating}/5"
