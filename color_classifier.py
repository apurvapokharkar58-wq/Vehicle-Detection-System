
import cv2
import numpy as np

def classify_vehicle_color(vehicle_image):

    if vehicle_image is None or vehicle_image.size == 0:
        return "Unknown"

    # Resize image
    image = cv2.resize(vehicle_image, (100, 100))

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Calculate average HSV values
    avg_hue = np.mean(hsv[:, :, 0])
    avg_saturation = np.mean(hsv[:, :, 1])
    avg_value = np.mean(hsv[:, :, 2])

    # Classify basic colours
    if avg_value < 60:
        return "Black"

    elif avg_saturation < 40:
        if avg_value > 190:
            return "White"
        else:
            return "Silver/Grey"

    elif avg_hue < 10 or avg_hue > 170:
        return "Red"

    elif 10 <= avg_hue < 25:
        return "Orange"

    elif 25 <= avg_hue < 35:
        return "Yellow"

    elif 35 <= avg_hue < 85:
        return "Green"

    elif 85 <= avg_hue < 130:
        return "Blue"

    elif 130 <= avg_hue <= 170:
        return "Purple"

    return "Unknown"
