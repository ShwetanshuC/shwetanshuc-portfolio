from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    from .models import WorkflowItem, WorkflowType
    items = WorkflowItem.objects.select_related("workflow_type", "stage", "assigned_to")
    if not request.user.is_staff:
        items = items.filter(assigned_to=request.user)
    context = {
        "items": items.order_by("-created_at")[:50],
        "workflow_types": list(WorkflowType.objects.filter(is_active=True)),
    }
    return render(request, "workflows/dashboard.html", context)
