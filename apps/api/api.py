"""
Django Ninja API instance and router configuration.
"""

from ninja import NinjaAPI

from apps.api.endpoints import detection, test_shots, training

api = NinjaAPI(
    title="License Plate Recognition API",
    version="1.0.0",
    description="API for license plate detection and training",
)

api.add_router("/test-shots/", test_shots.router, tags=["Test Shots"])
api.add_router("/detection/", detection.router, tags=["Detection"])
api.add_router("/training-shots/", training.router, tags=["Training"])
