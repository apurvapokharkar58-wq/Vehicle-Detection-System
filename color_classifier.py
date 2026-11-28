
import cv2
import numpy as np


def classify_vehicle_color(vehicle_image):

    if vehicle_image is None or vehicle_image.size == 0:
        return "Unknown"

    # Resize vehicle image
    image = cv2.resize(vehicle_image, (100, 100))

    # Use central region to reduce background interference
    h, w = image.shape[:2]

    crop = image[
        int(h * 0.20):int(h * 0.80),
        int(w * 0.20):int(w * 0.80)
    ]

    # Convert BGR to HSV
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    median_value = np.median(value)
    median_saturation = np.median(saturation)

    # Handle black, white and grey first
    if median_value < 60:
        return "Black"

    elif median_saturation < 40:
        if median_value > 190:
            return "White"
        else:
            return "Silver/Grey"

    # Select colorful pixels
    valid_pixels = (value > 45) & (saturation > 35)

    if np.count_nonzero(valid_pixels) < 20:
        return "Silver/Grey"

    # Calculate median hue using valid pixels
    avg_hue = np.median(hsv[:, :, 0][valid_pixels])

    # Classify color
    if avg_hue < 10 or avg_hue > 170:
        return "Red"

    elif avg_hue < 25:
        return "Orange"

    elif avg_hue < 35:
        return "Yellow"

    elif avg_hue < 85:
        return "Green"

    elif avg_hue < 130:
        return "Blue"

    elif avg_hue <= 170:
        return "Purple"

    return "Unknown"
