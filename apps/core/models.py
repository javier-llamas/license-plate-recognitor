"""
Core database models for license plate recognition system.
"""

from django.db import models


class TestShot(models.Model):
    """Stores test shots taken manually by the user."""

    image_path = models.CharField(
        max_length=500, help_text="Relative path in media volume"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"TestShot {self.id} - {self.created_at}"


class DetectionResult(models.Model):
    """Stores individual detection results from running jobs."""

    workflow_id = models.CharField(
        max_length=200, help_text="DBOS workflow ID that created this detection"
    )
    image_path = models.CharField(max_length=500)
    plate_text = models.CharField(max_length=50, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    camera_model = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["workflow_id"]),
        ]

    def __str__(self):
        return f"Detection {self.id} - {self.plate_text or 'No plate'}"


class TrainingShot(models.Model):
    """Stores shots for training/evaluation with user corrections."""

    image_path = models.CharField(max_length=500)
    inferred_text = models.CharField(
        max_length=50, null=True, blank=True, help_text="Text inferred by the model"
    )
    actual_text = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Corrected text provided by user",
    )
    is_verified = models.BooleanField(default=False)
    is_accurate = models.BooleanField(
        null=True, blank=True, help_text="True if green checkmark, False if red X"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"TrainingShot {self.id} - {'Verified' if self.is_verified else 'Unverified'}"
