"""
Detection job API endpoints.

Uses DBOS client to start and cancel workflows directly.
DBOS manages workflow state in its own system tables.
"""

import os

from dbos import DBOSClient, EnqueueOptions
from ninja import Router

from apps.api.schemas import (
    DetectionJobStartResponse,
    DetectionJobStatusResponse,
    DetectionJobStopResponse,
)
from apps.core.models import DetectionResult

router = Router()

# Initialize DBOS client for workflow management
# This connects to the DBOS system database where workflow state is stored
dbos_client = DBOSClient(system_database_url=os.environ.get("DBOS_DATABASE_URL"))


@router.post("/start", response=DetectionJobStartResponse)
def start_detection(request):
    """Start a detection job via DBOS workflow."""
    try:
        # Check if there's already a running detection workflow
        running_workflows = dbos_client.list_workflows(
            name="start_detection_workflow",
            status="PENDING",  # DBOS workflow status for running workflows
        )
        if running_workflows:
            return {"error": "A detection job is already running"}, 400

        # Start the detection workflow via DBOS client
        # This enqueues the workflow for execution by the cv worker
        options: EnqueueOptions = {
            "workflow_name": "start_detection_workflow",
            "queue_name": "detection_queue",
        }
        handle = dbos_client.enqueue(options)

        workflow_id = handle.get_workflow_id()

        return DetectionJobStartResponse(status="running", workflow_id=workflow_id)
    except Exception as e:
        return {"error": str(e)}, 500


@router.post("/stop", response=DetectionJobStopResponse)
def stop_detection(request):
    """Stop the currently running detection job."""
    try:
        # Find the running detection workflow
        running_workflows = dbos_client.list_workflows(
            name="start_detection_workflow", status="PENDING"
        )

        if not running_workflows:
            return {"error": "No detection job is running"}, 400

        # Cancel the workflow via DBOS client
        # DBOS will interrupt the workflow at the beginning of its next step
        workflow_id = running_workflows[0].workflow_id
        dbos_client.cancel_workflow(workflow_id)

        return DetectionJobStopResponse(workflow_id=workflow_id, status="stopped")
    except Exception as e:
        return {"error": str(e)}, 500


@router.get("/status", response=DetectionJobStatusResponse)
def get_detection_status(request):
    """Get current detection job status."""
    try:
        # Query DBOS for running detection workflows
        running_workflows = dbos_client.list_workflows(
            name="start_detection_workflow", status="PENDING"
        )

        if running_workflows:
            workflow_id = running_workflows[0].workflow_id

            # Get the most recent detection result for this workflow
            recent_result = DetectionResult.objects.filter(
                workflow_id=workflow_id
            ).first()

            return DetectionJobStatusResponse(
                is_running=True,
                current_job={
                    "workflow_id": workflow_id,
                    "started_at": running_workflows[0].created_at,
                    "latest_detection": (
                        recent_result.created_at if recent_result else None
                    ),
                },
            )
        else:
            return DetectionJobStatusResponse(is_running=False, current_job=None)
    except Exception as e:
        return {"error": str(e)}, 500
