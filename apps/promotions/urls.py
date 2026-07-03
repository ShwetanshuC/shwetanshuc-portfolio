from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="promotions_index"),
    path("<slug:slug>/", views.detail, name="promotion_detail"),
    path("<slug:slug>/items/", views.promotion_catalog, name="promotion_catalog"),
]
