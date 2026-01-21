"""
Camera interface using picamera2 for Raspberry Pi 5.
"""

from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

from picamera2 import Picamera2


class Camera:
    """Camera interface for capturing images."""

    def __init__(self):
        self.camera = Picamera2()
        config = self.camera.create_still_configuration()
        self.camera.configure(config)
        self.camera.start()
        self.camera_model = "Raspberry Pi Camera"

    def capture_image(self) -> np.ndarray:
        """
        Capture an image and return as numpy array.
        Returns RGB image array.
        """
        # Capture as numpy array
        array = self.camera.capture_array()
        return array

    def _create_mock_image(self) -> np.ndarray:
        """Create a mock image for development/testing."""
        # Create a simple test pattern
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        img[:, :] = [100, 150, 200]  # Light blue background
        return img

    def save_image(
        self, image: np.ndarray, directory: str, filename: str | None = None
    ) -> str:
        """
        Save image to specified directory.
        Returns the relative path.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.jpg"

        # Ensure directory exists
        dir_path = Path("/app/media") / directory
        dir_path.mkdir(parents=True, exist_ok=True)

        # Full path for saving
        full_path = dir_path / filename

        # Convert RGB to BGR for OpenCV
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        else:
            image_bgr = image

        # Save image
        cv2.imwrite(str(full_path), image_bgr)

        # Return relative path
        return f"{directory}/{filename}"

    def capture_and_save(
        self, directory: str, filename: str | None = None
    ) -> tuple[np.ndarray, str]:
        """
        Capture an image and save it.
        Returns (image_array, relative_path).
        """
        image = self.capture_image()
        path = self.save_image(image, directory, filename)
        return image, path

    def get_camera_model(self) -> str:
        """Return the camera model string."""
        return self.camera_model

    def cleanup(self):
        """Clean up camera resources."""
        self.camera.stop()
        self.camera.close()


# Global camera instance
_camera_instance = None


def get_camera() -> Camera:
    """Get or create the global camera instance."""
    global _camera_instance
    if _camera_instance is None:
        _camera_instance = Camera()
    return _camera_instance
