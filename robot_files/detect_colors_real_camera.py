import cv2
import numpy as np
import time

# The real camera setup replaces the PyBullet simulation
print("Initializing camera...")
cap = cv2.VideoCapture(0)  # Try 0, 1, or 2 if one doesn't work

# Give camera time to warm up
time.sleep(2)

def gray_world_balance(img_bgr):
    img = img_bgr.astype(np.float32)
    b, g, r = cv2.split(img)
    mean_b, mean_g, mean_r = b.mean(), g.mean(), r.mean()
    gray = (mean_b + mean_g + mean_r) / 3.0

    b *= gray / (mean_b + 1e-6)
    g *= gray / (mean_g + 1e-6)
    r *= gray / (mean_r + 1e-6)

    balanced = cv2.merge([b, g, r])
    return np.clip(balanced, 0, 255).astype(np.uint8)

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# Capture a frame
print("Capturing image...")
ret, bgr_image = cap.read()
bgr_image = gray_world_balance(bgr_image)

if not ret:
    print("ERROR: Could not read from camera!")
    cap.release()
    exit()

print(f"Image captured: {bgr_image.shape}")

# Color detection remains the same as in the PyBullet version but adapted for real camera images
# Convert to HSV color space (better for color detection)
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# Define color ranges in HSV
# NOTE: Ranges may need to be adjusted based on the lighting
color_ranges = {
    'red1': {
        'lower': np.array([0, 50, 50]),
        'upper': np.array([10, 255, 255]),
        'display_color': (0, 0, 255)
    },
    'red2': {
        'lower': np.array([170, 50, 50]),
        'upper': np.array([180, 255, 255]),
        'display_color': (0, 0, 255)
    },
    'green': {
        'lower': np.array([50, 20, 40]),     # Lower bound for green in HSV
        'upper': np.array([70, 240, 240]),     # Upper bound for green in HSV
        'display_color': (0, 255, 0)           # BGR for drawing (green)
    },
    'blue': {
        'lower': np.array([90, 30, 30]),
        'upper': np.array([140, 255, 255]),
        'display_color': (255, 0, 0)
    },
}

# Create a copy of the image to draw on
output_image = bgr_image.copy()

# Detect each color
detected_objects = []

for color_name, color_info in color_ranges.items():
    # Create a mask for this color
    mask = cv2.inRange(hsv_image, color_info['lower'], color_info['upper'])

    # Find contours (outlines) of colored regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process each contour
    for contour in contours:
        area = cv2.contourArea(contour)

        # Filter out small noise (only keep objects bigger than 500 pixels)
        if area > 500:  # Increased threshold for real camera
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Calculate center point
            center_x = x + w // 2
            center_y = y + h // 2

            # Draw bounding box
            cv2.rectangle(output_image, (x, y), (x + w, y + h),
                         color_info['display_color'], 2)

            # Draw center point
            cv2.circle(output_image, (center_x, center_y), 5,
                      color_info['display_color'], -1)

            # Add label
            cv2.putText(output_image, color_name.upper(), (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_info['display_color'], 2)

            # Store detection info
            detected_objects.append({
                'color': color_name,
                'position': (center_x, center_y),
                'bounding_box': (x, y, w, h),
                'area': area
            })

            print(f"Found {color_name} object at position ({center_x}, {center_y})")
            print(f"Size: {w}x{h} pixels, Area: {area} pixels²")

print(f"\nTotal objects detected: {len(detected_objects)}")

# Save the annotated image
cv2.imwrite('color_detection_result_real.png', output_image)
print("\n Annotated image saved as 'color_detection_result_real.png'")

# Also save the original for comparison
cv2.imwrite('original_image_real.png', bgr_image)
print("Original image saved as 'original_image_real.png'")

# Display the result
cv2.imshow('Detected Colors', output_image)
print("\nPress any key to close...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# Clean up
cap.release()
print("Done!")