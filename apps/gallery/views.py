from django.shortcuts import render
from .models import GalleryPhoto, GalleryVideo


def gallery(request):
    photos = GalleryPhoto.objects.filter(is_active=True)
    videos = GalleryVideo.objects.filter(is_active=True)
    context = {"photos": photos, "videos": videos}
    return render(request, "gallery/gallery.html", context)
