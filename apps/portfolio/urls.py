from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("music/", views.music, name="music"),
    path("web-development/", views.web_dev, name="web_dev"),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("before-after/", views.before_after, name="before_after"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
]
