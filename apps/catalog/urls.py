from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="catalog_index"),
    path("category/<slug:slug>/", views.by_category, name="catalog_by_category"),
    path("<slug:slug>/", views.detail, name="catalog_detail"),
]
