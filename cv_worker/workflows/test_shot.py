"""
Test shot workflow - captures a single image on demand.
"""

import logfire
from dbos import DBOS

from apps.core.models import TestShot
from cv_worker.camera import get_camera


@DBOS.workflow()
def test_shot_workflow():
    """
    Workflow to capture a test shot.
    Returns the TestShot ID.
    """
    logfire.info("Starting test shot workflow")

    # Capture and save image
    test_shot_id = capture_test_shot()

    logfire.info(f"Test shot workflow completed: {test_shot_id}")
    return test_shot_id


@DBOS.step()
def capture_test_shot() -> int:
    """
    Step to capture and save a test shot.
    Returns the TestShot ID.
    """
    camera = get_camera()

    # Capture and save image
    image, image_path = camera.capture_and_save("test_shots")

    # Create database record
    test_shot = TestShot.objects.create(image_path=image_path)

    logfire.info(f"Test shot captured: {test_shot.pk} at {image_path}")

    return test_shot.pk
