from django.db import models


class GalleryPhoto(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="gallery/photos/")
    image_focal_y = models.FloatField(default=0.5)
    mobile_image = models.ImageField(upload_to="gallery/mobile/", blank=True, null=True)
    mobile_focal_y = models.FloatField(default=0.5)
    caption = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"

    def __str__(self):
        return self.title or f"Photo #{self.pk}"


class GalleryVideo(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField(help_text="YouTube or Vimeo URL")
    thumbnail = models.ImageField(upload_to="gallery/thumbnails/", blank=True, null=True)
    caption = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Gallery Video"
        verbose_name_plural = "Gallery Videos"

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        url = self.video_url
        if not url:
            return url
        # Handle youtu.be shortlinks
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        # Handle youtube.com/watch?v=
        if "youtube.com/watch" in url:
            return url.replace("watch?v=", "embed/").split("&")[0]
        # Handle Vimeo
        if "vimeo.com/" in url:
            video_id = url.rstrip("/").split("/")[-1]
            return f"https://player.vimeo.com/video/{video_id}"
        return url
