"""
Detection job workflow - continuous license plate detection with 2-second interval.

DBOS manages workflow state in its own system tables.
Each detection is a separate step, allowing DBOS to cancel between iterations.
"""

import logging
import time

# import logfire
from dbos import DBOS

from apps.core.models import DetectionResult, TrainingShot
from cv_worker.camera import get_camera
from cv_worker.detector import get_detector

logfire = logging.getLogger(__name__)


@DBOS.workflow()
def start_detection_workflow():
    """
    Start a continuous detection workflow.

    Returns workflow_id for cancellation.
    DBOS manages the workflow state - no custom job table needed.
    """
    workflow_id = DBOS.workflow_id
    logfire.info(f"Starting detection workflow: {workflow_id}")

    # Run detection loop - each iteration is a cancellable step
    iteration = 0
    while True:
        iteration += 1

        # Perform single detection (this is a step, so it can be cancelled between iterations)
        perform_single_detection()

        # Sleep between detections
        time.sleep(2)


@DBOS.step()
def perform_single_detection():
    """
    Perform a single detection step.

    This is a separate step so DBOS can cancel the workflow between detections.
    Saves result to Django DB with workflow_id for tracking.
    """
    workflow_id = DBOS.workflow_id
    try:
        camera = get_camera()
        detector = get_detector()

        # Capture image
        image, image_path = camera.capture_and_save("detections")

        # Detect license plate
        plate_text, confidence = detector.detect(image)

        # Save detection result with workflow_id
        DetectionResult.objects.create(
            workflow_id=workflow_id,
            image_path=image_path,
            plate_text=plate_text,
            confidence=confidence,
            camera_model=camera.get_camera_model(),
        )

        # Create training shot for evaluation
        TrainingShot.objects.create(
            image_path=image_path, inferred_text=plate_text, is_verified=False
        )

        logfire.info(
            f"Detection for workflow {workflow_id}: "
            f"{plate_text or 'No plate'} (confidence: {confidence})"
        )

    except Exception as e:
        logfire.error(f"Error in detection step: {e}")
        # Don't fail the workflow, just log the error
        # DBOS will continue to next iteration
