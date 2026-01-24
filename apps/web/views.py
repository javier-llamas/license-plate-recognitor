"""
HTMX views for the web interface.
"""

import os
from typing import TYPE_CHECKING
import logging

from dbos import DBOSClient, EnqueueOptions
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.core.models import DetectionResult, TestShot, TrainingShot
from cv_worker.workflows.test_shot import test_shot_workflow

if TYPE_CHECKING:
    from dbos import WorkflowHandle
    from django.http import HttpRequest

logger = logging.getLogger(__name__)

# Initialize DBOS client for workflow management
dbos_client = DBOSClient(system_database_url=os.environ.get("DBOS_DATABASE_URL"))


def home(request: "HttpRequest") -> HttpResponse:
    """Home page with detection job controls."""
    # Check DBOS for running detection workflows
    running_workflows = dbos_client.list_workflows(
        name="start_detection_workflow", status="PENDING"
    )

    is_running = len(running_workflows) > 0
    recent_results = None
    workflow_id = None

    if is_running:
        workflow_id = running_workflows[0].workflow_id
        recent_results = DetectionResult.objects.filter(
            workflow_id=workflow_id
        ).order_by("-created_at")[:10]

    context = {
        "is_running": is_running,
        "workflow_id": workflow_id,
        "recent_results": recent_results,
    }
    return render(request, "home.html", context)


def test_shot_page(request: "HttpRequest", test_shot_id: int) -> HttpResponse:
    """Display a test shot."""
    test_shot = get_object_or_404(TestShot, id=test_shot_id)
    context = {
        "test_shot": test_shot,
        "image_url": f"{settings.MEDIA_URL}{test_shot.image_path}",
    }
    return render(request, "test_shot.html", context)


def evaluate_page(request: "HttpRequest") -> HttpResponse:
    """Evaluation page for training shots."""
    shot = TrainingShot.objects.filter(is_verified=False).first()

    context: dict[str, TrainingShot | None | str] = {
        "shot": shot,
    }

    if shot:
        context["image_url"] = f"{settings.MEDIA_URL}{shot.image_path}"

    return render(request, "evaluate.html", context)


# HTMX partial views
def take_test_shot(request: "HttpRequest") -> HttpResponse:
    """HTMX endpoint to trigger test shot."""
    try:
        # Start test shot workflow via DBOS client
        options: EnqueueOptions = {
            "workflow_name": "test_shot_workflow",
            "queue_name": "test_shot_queue",
        }
        shot_d = test_shot_workflow()

        # Wait for result (test shots are quick)
        # logger.info(f"Waiting for test shot workflow: {handle.workflow_id}")
        logger.info(f"DBOS System DB URL: {os.environ.get('DBOS_DATABASE_URL')}")
        # test_shot_id = handle

        # Return HTML snippet to redirect
        return HttpResponse(
            f'<script>window.location.href="/test-shot/{shot_d}";</script>'
        )
    except Exception as e:
        return HttpResponse(f'<div class="error">Error: {str(e)}</div>')


def toggle_detection(request: "HttpRequest") -> HttpResponse:
    """HTMX endpoint to start/stop detection."""
    # Check for running detection workflows
    running_workflows = dbos_client.list_workflows(
        name="start_detection_workflow", status="PENDING"
    )

    try:
        if running_workflows:
            # Stop detection by cancelling the workflow
            workflow_id = running_workflows[0].workflow_id
            dbos_client.cancel_workflow(workflow_id)

            return HttpResponse(
                '<button hx-post="/toggle-detection" hx-swap="outerHTML">Start</button>'
            )
        else:
            # Start detection
            options: EnqueueOptions = {
                "workflow_name": "start_detection_workflow",
                "queue_name": "detection_queue",
            }
            dbos_client.enqueue(options)

            return HttpResponse(
                '<button hx-post="/toggle-detection" hx-swap="outerHTML">Stop</button>'
            )
    except Exception as e:
        return HttpResponse(f'<div class="error">Error: {str(e)}</div>')
