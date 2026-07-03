from django.conf import settings
from django.db import models


class WorkflowType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Workflow Type"
        verbose_name_plural = "Workflow Types"

    def __str__(self):
        return self.name


class WorkflowStage(models.Model):
    workflow_type = models.ForeignKey(
        WorkflowType, on_delete=models.CASCADE, related_name="stages"
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_terminal = models.BooleanField(
        default=False, help_text="Final stage — no further progression"
    )

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Workflow Stage"
        verbose_name_plural = "Workflow Stages"
        unique_together = [("workflow_type", "name")]

    def __str__(self):
        return f"{self.workflow_type.name} → {self.name}"


class WorkflowItem(models.Model):
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_URGENT = "urgent"
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
        (PRIORITY_URGENT, "Urgent"),
    ]

    title = models.CharField(max_length=200)
    workflow_type = models.ForeignKey(
        WorkflowType, on_delete=models.PROTECT, related_name="items"
    )
    stage = models.ForeignKey(
        WorkflowStage, on_delete=models.PROTECT, related_name="items"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_workflows",
    )
    requester_name = models.CharField(max_length=120, blank=True)
    requester_email = models.EmailField(blank=True)
    requester_phone = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    due_date = models.DateField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True, help_text="Store any additional structured data")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Workflow Item"
        verbose_name_plural = "Workflow Items"

    def __str__(self):
        return self.title


class WorkflowNote(models.Model):
    item = models.ForeignKey(WorkflowItem, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="workflow_notes",
    )
    content = models.TextField()
    is_internal = models.BooleanField(
        default=True, help_text="Internal notes not visible to requester"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Workflow Note"
        verbose_name_plural = "Workflow Notes"

    def __str__(self):
        return f"Note on {self.item.title}"
