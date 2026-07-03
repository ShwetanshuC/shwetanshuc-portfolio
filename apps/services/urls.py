from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="services_index"),
    path("<slug:slug>/", views.detail, name="service_detail"),
]
