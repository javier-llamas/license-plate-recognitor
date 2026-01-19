"""
Django admin configuration for core models.
"""

from django.contrib import admin

from .models import DetectionJob, DetectionResult, TestShot, TrainingShot


@admin.register(TestShot)
class TestShotAdmin(admin.ModelAdmin):
    list_display = ["id", "image_path", "created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]


@admin.register(DetectionJob)
class DetectionJobAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "started_at", "stopped_at", "workflow_id"]
    list_filter = ["status", "started_at"]
    readonly_fields = ["started_at", "stopped_at"]


@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "job",
        "plate_text",
        "confidence",
        "camera_model",
        "created_at",
    ]
    list_filter = ["created_at", "job"]
    readonly_fields = ["created_at"]
    search_fields = ["plate_text"]


@admin.register(TrainingShot)
class TrainingShotAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "inferred_text",
        "actual_text",
        "is_verified",
        "is_accurate",
        "created_at",
    ]
    list_filter = ["is_verified", "is_accurate", "created_at"]
    readonly_fields = ["created_at"]
    search_fields = ["inferred_text", "actual_text"]
