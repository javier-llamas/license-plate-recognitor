"""
Django admin configuration for core models.
"""

from django.contrib import admin

from .models import DetectionResult, TestShot, TrainingShot


@admin.register(TestShot)
class TestShotAdmin(admin.ModelAdmin):
    list_display = ["id", "image_path", "created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]


@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "workflow_id",
        "plate_text",
        "confidence",
        "camera_model",
        "created_at",
    ]
    list_filter = ["created_at", "workflow_id"]
    readonly_fields = ["created_at"]
    search_fields = ["plate_text", "workflow_id"]


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
