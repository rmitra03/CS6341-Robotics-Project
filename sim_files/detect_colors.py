import pybullet as p
import time
import numpy as np
from PIL import Image
import cv2

# Start PyBullet
p.connect(p.GUI)
p.setGravity(0, 0, -9.81)

# Create floor
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(baseCollisionShapeIndex=floor_shape, basePosition=[0, 0, 0])

# Create shapes with distinct colors
print("Creating shapes...")

# Red square
square_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025])
square_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025], 
                                    rgbaColor=[1, 0, 0, 1])  # Pure red
red_square = p.createMultiBody(baseMass=0.1,
                               baseCollisionShapeIndex=square_collision,
                               baseVisualShapeIndex=square_visual,
                               basePosition=[0, 0, 0.5])

# Green circle
circle_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.05, height=0.05)
circle_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.05, length=0.05,
                                    rgbaColor=[0, 1, 0, 1])  # Pure green
green_circle = p.createMultiBody(baseMass=0.1,
                                 baseCollisionShapeIndex=circle_collision,
                                 baseVisualShapeIndex=circle_visual,
                                 basePosition=[0.2, 0, 0.5])

# Blue triangle
triangle_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025])
triangle_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025],
                                      rgbaColor=[0, 0, 1, 1])  # Pure blue
blue_triangle = p.createMultiBody(baseMass=0.1,
                                  baseCollisionShapeIndex=triangle_collision,
                                  baseVisualShapeIndex=triangle_visual,
                                  basePosition=[0.4, 0, 0.5])

# Let shapes settle
print("Letting shapes settle...")
for i in range(200):
    p.stepSimulation()
    time.sleep(1./240.)

# Camera setup
camera_position = [0.2, -0.5, 0.5]
target_position = [0.2, 0, 0.05]
up_vector = [0, 0, 1]

width = 640
height = 480
fov = 60
aspect = width / height
near = 0.1
far = 3.0

view_matrix = p.computeViewMatrix(
    cameraEyePosition=camera_position,
    cameraTargetPosition=target_position,
    cameraUpVector=up_vector
)

projection_matrix = p.computeProjectionMatrixFOV(
    fov=fov,
    aspect=aspect,
    nearVal=near,
    farVal=far
)

# Take a picture
print("Taking picture...")
img_data = p.getCameraImage(
    width=width,
    height=height,
    viewMatrix=view_matrix,
    projectionMatrix=projection_matrix,
    renderer=p.ER_BULLET_HARDWARE_OPENGL
)

# Convert to OpenCV format
rgb_array = np.array(img_data[2], dtype=np.uint8)
rgb_array = rgb_array.reshape((height, width, 4))
rgb_array = rgb_array[:, :, :3]

# Convert RGB to BGR (OpenCV uses BGR)
bgr_image = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)

# Convert to HSV color space (better for color detection)
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# Define color ranges in HSV
# HSV is better than RGB for color detection because it separates color from brightness
color_ranges = {
    'red': {
        'lower': np.array([0, 100, 100]),      # Lower bound for red in HSV
        'upper': np.array([10, 255, 255]),     # Upper bound for red in HSV
        'display_color': (0, 0, 255)           # BGR for drawing (red)
    },
    'green': {
        'lower': np.array([40, 100, 100]),     # Lower bound for green in HSV
        'upper': np.array([80, 255, 255]),     # Upper bound for green in HSV
        'display_color': (0, 255, 0)           # BGR for drawing (green)
    },
    'blue': {
        'lower': np.array([100, 100, 100]),    # Lower bound for blue in HSV
        'upper': np.array([130, 255, 255]),    # Upper bound for blue in HSV
        'display_color': (255, 0, 0)           # BGR for drawing (blue)
    }
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
        
        # Filter out small noise (only keep objects bigger than 100 pixels)
        if area > 100:
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
            
            print(f"✓ Found {color_name} object at position ({center_x}, {center_y})")
            print(f"  Size: {w}x{h} pixels, Area: {area} pixels²")

print(f"\nTotal objects detected: {len(detected_objects)}")

# Save the annotated image
cv2.imwrite('color_detection_result.png', output_image)
print("\nAnnotated image saved as 'color_detection_result.png'")

# Also save the original for comparison
cv2.imwrite('original_image.png', bgr_image)

# Keep simulation running
print("\nSimulation running. Close window to exit.")
try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    print("Closing...")
    p.disconnect()