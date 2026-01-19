"""
Test shots API endpoints.
"""

import os

from dbos import DBOSClient, EnqueueOptions
from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import Router

from apps.api.schemas import TestShotCreateResponse, TestShotResponse
from apps.core.models import TestShot

router = Router()

# Initialize DBOS client for workflow management
dbos_client = DBOSClient(system_database_url=os.environ.get("DBOS_DATABASE_URL"))


@router.post("/", response=TestShotCreateResponse)
def create_test_shot(request):
    """Trigger a test shot capture via DBOS workflow."""
    try:
        # Start test shot workflow via DBOS client
        options: EnqueueOptions = {
            "workflow_name": "test_shot_workflow",
            "queue_name": "test_shot_queue",
        }
        handle = dbos_client.enqueue(options)

        # Wait for result (test shots are quick)
        test_shot_id = handle.get_result()

        return TestShotCreateResponse(id=test_shot_id, status="processing")
    except Exception as e:
        return {"error": str(e)}, 500


@router.get("/{test_shot_id}", response=TestShotResponse)
def get_test_shot(request, test_shot_id: int):
    """Get test shot details."""
    test_shot = get_object_or_404(TestShot, id=test_shot_id)

    return TestShotResponse(
        id=test_shot.id,
        image_url=f"{settings.MEDIA_URL}{test_shot.image_path}",
        created_at=test_shot.created_at,
        status="ready",
    )
