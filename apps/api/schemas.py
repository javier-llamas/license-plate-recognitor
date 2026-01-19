"""
Pydantic schemas for API request/response validation.
"""

from datetime import datetime
from typing import Optional

from ninja import Schema


# Test Shots Schemas
class TestShotResponse(Schema):
    id: int
    image_url: str
    created_at: datetime
    status: str


class TestShotCreateResponse(Schema):
    id: int
    status: str


# Detection Job Schemas (DBOS workflow-based)
class DetectionJobStartResponse(Schema):
    status: str
    workflow_id: str


class DetectionJobStopResponse(Schema):
    workflow_id: str
    status: str


class DetectionJobStatusResponse(Schema):
    is_running: bool
    current_job: Optional[dict] = None


# Training Shots Schemas
class TrainingShotResponse(Schema):
    id: int
    image_url: str
    inferred_text: Optional[str] = None


class TrainingShotVerifyRequest(Schema):
    is_accurate: bool
    actual_text: Optional[str] = None


class TrainingShotVerifyResponse(Schema):
    id: int
    is_verified: bool
