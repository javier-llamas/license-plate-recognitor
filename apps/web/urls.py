"""
URL configuration for web interface.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test-shot/<int:test_shot_id>/", views.test_shot_page, name="test_shot"),
    path("evaluate/", views.evaluate_page, name="evaluate"),
    # HTMX endpoints
    path("take-test-shot/", views.take_test_shot, name="take_test_shot"),
    path("toggle-detection/", views.toggle_detection, name="toggle_detection"),
]
