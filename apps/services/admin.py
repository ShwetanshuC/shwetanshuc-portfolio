from django.contrib import admin
from .models import Service, ServiceFeature, ServiceAppointment


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    fields = ["feature", "sort_order"]
    extra = 2


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["sort_order", "name", "price_display", "is_featured", "is_active"]
    list_editable = ["is_featured", "is_active", "sort_order"]
    list_display_links = ["name"]
    list_filter = ["is_featured", "is_active"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceFeatureInline]
    ordering = ["sort_order", "name"]


@admin.register(ServiceAppointment)
class ServiceAppointmentAdmin(admin.ModelAdmin):
    list_display = ["customer_name", "service", "status", "preferred_date", "created_at"]
    list_editable = ["status"]
    list_display_links = ["customer_name"]
    list_filter = ["status", "service"]
    search_fields = ["customer_name", "customer_email", "notes"]
    readonly_fields = ["created_at", "updated_at"]
