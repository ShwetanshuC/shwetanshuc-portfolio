from django.urls import path
from . import views

urlpatterns = [
    path("contact/", views.contact, name="contact"),
    path("item/<slug:item_slug>/", views.item_inquiry, name="item_inquiry"),
    path("service/<slug:service_slug>/", views.service_inquiry, name="service_inquiry"),
    path("quote/", views.quote_request, name="quote_request"),
    path("thank-you/", views.thank_you, name="inquiry_thank_you"),
]
