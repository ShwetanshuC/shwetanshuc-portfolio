from django.contrib import admin
from .models import WorkflowType, WorkflowStage, WorkflowItem, WorkflowNote


class WorkflowStageInline(admin.TabularInline):
    model = WorkflowStage
    fields = ["name", "description", "sort_order", "is_terminal"]
    extra = 2


class WorkflowNoteInline(admin.TabularInline):
    model = WorkflowNote
    fields = ["author", "content", "is_internal"]
    extra = 1
    readonly_fields = ["created_at"]


@admin.register(WorkflowType)
class WorkflowTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    list_editable = ["is_active"]
    inlines = [WorkflowStageInline]


@admin.register(WorkflowItem)
class WorkflowItemAdmin(admin.ModelAdmin):
    list_display = ["title", "workflow_type", "stage", "assigned_to", "priority", "due_date", "created_at"]
    list_filter = ["workflow_type", "stage", "priority", "assigned_to"]
    search_fields = ["title", "requester_name", "requester_email", "description"]
    inlines = [WorkflowNoteInline]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Item", {"fields": ("title", "workflow_type", "stage", "priority", "due_date")}),
        ("Assignment", {"fields": ("assigned_to",)}),
        ("Requester", {"fields": ("requester_name", "requester_email", "requester_phone")}),
        ("Details", {"fields": ("description", "metadata")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
