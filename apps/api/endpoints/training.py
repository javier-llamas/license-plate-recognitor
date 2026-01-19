"""
Training shots API endpoints.
"""

from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import Router

from apps.api.schemas import (
    TrainingShotResponse,
    TrainingShotVerifyRequest,
    TrainingShotVerifyResponse,
)
from apps.core.models import TrainingShot

router = Router()


@router.get("/next-unverified", response=TrainingShotResponse)
def get_next_unverified(request):
    """Get the next unverified training shot."""
    shot = TrainingShot.objects.filter(is_verified=False).first()

    if not shot:
        return None

    return TrainingShotResponse(
        id=shot.id,
        image_url=f"{settings.MEDIA_URL}{shot.image_path}",
        inferred_text=shot.inferred_text,
    )


@router.post("/{shot_id}/verify", response=TrainingShotVerifyResponse)
def verify_training_shot(request, shot_id: int, payload: TrainingShotVerifyRequest):
    """Mark a training shot as accurate or inaccurate with optional correction."""
    shot = get_object_or_404(TrainingShot, id=shot_id)

    shot.is_verified = True
    shot.is_accurate = payload.is_accurate

    if not payload.is_accurate and payload.actual_text:
        shot.actual_text = payload.actual_text

    shot.save()

    return TrainingShotVerifyResponse(id=shot.id, is_verified=True)
