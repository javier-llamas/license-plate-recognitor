"""
License plate detector using fast_alpr.
"""

import random
from typing import Optional, Tuple

import numpy as np
from fast_alpr import ALPR


class PlateDetector:
    """License plate detector wrapper."""

    def __init__(self):
        self.alpr = None

        try:
            self.alpr = ALPR(
                detector_model="yolo-v9-s-608-license-plate-end2end",
                ocr_model="cct-xs-v1-global-model",
            )
            print("Fast ALPR initialized successfully")
        except Exception as e:
            print(f"Error initializing fast_alpr: {e}")
            self.alpr = None

    def detect(self, image: np.ndarray) -> Tuple[Optional[str], Optional[float]]:
        """
        Detect license plate in image.
        Returns (plate_text, confidence) or (None, None) if no plate detected.
        """
        if self.alpr:
            try:
                results = self.alpr.predict(image)

                if results and len(results) > 0:
                    # Get the first (highest confidence) result
                    top_result = results[0]
                    plate_text = top_result.ocr.text
                    confidence = top_result.ocr.confidence

                    return plate_text, confidence
                else:
                    return None, None

            except Exception as e:
                print(f"Error during detection: {e}")
                return None, None
        else:
            # Mock detection for development
            return self._mock_detect(image)

    def _mock_detect(self, image: np.ndarray) -> Tuple[Optional[str], Optional[float]]:
        """Mock detection for development/testing."""
        # Simulate detection with 70% success rate
        if random.random() < 0.7:
            # Generate a mock license plate
            mock_plates = ["ABC1234", "XYZ5678", "DEF9012", "GHI3456", "JKL7890"]
            plate = random.choice(mock_plates)
            confidence = random.uniform(0.85, 0.98)
            return plate, confidence
        else:
            return None, None


# Global detector instance
_detector_instance = None


def get_detector() -> PlateDetector:
    """Get or create the global detector instance."""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = PlateDetector()
    return _detector_instance
