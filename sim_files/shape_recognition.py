import pybullet as p
import time
import numpy as np
import cv2

# Start PyBullet
p.connect(p.GUI)
p.setGravity(0, 0, -9.81)

# Create floor
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(baseCollisionShapeIndex=floor_shape, basePosition=[0, 0, 0])

print("Creating shapes for recognition...")

# Create shapes with distinct colors
# Red square
square_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025])
square_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025], 
                                    rgbaColor=[1, 0, 0, 1])
red_square = p.createMultiBody(baseMass=0.5,
                               baseCollisionShapeIndex=square_collision,
                               baseVisualShapeIndex=square_visual,
                               basePosition=[0, 0, 0.5])

# Green circle
circle_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.05, height=0.05)
circle_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.05, length=0.05,
                                    rgbaColor=[0, 1, 0, 1])
green_circle = p.createMultiBody(baseMass=0.5,
                                 baseCollisionShapeIndex=circle_collision,
                                 baseVisualShapeIndex=circle_visual,
                                 basePosition=[0.2, 0, 0.5])

# Blue triangle (using box for now)
triangle_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025])
triangle_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025],
                                      rgbaColor=[0, 0, 1, 1])
blue_triangle = p.createMultiBody(baseMass=0.5,
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
bgr_image = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# Define color ranges
color_ranges = {
    'red': {
        'lower': np.array([0, 100, 100]),
        'upper': np.array([10, 255, 255]),
        'display_color': (0, 0, 255)
    },
    'green': {
        'lower': np.array([40, 100, 100]),
        'upper': np.array([80, 255, 255]),
        'display_color': (0, 255, 0)
    },
    'blue': {
        'lower': np.array([100, 100, 100]),
        'upper': np.array([130, 255, 255]),
        'display_color': (255, 0, 0)
    }
}

def calculate_shape_features(contour):
    """
    Calculate multiple geometric features for robust shape classification
    """
    # Basic measurements
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    
    if perimeter == 0:
        return None
    
    # Circularity: how close to a perfect circle (1.0 = perfect circle)
    circularity = 4 * np.pi * area / (perimeter * perimeter)
    
    # Approximate polygon
    epsilon = 0.04 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)
    vertices = len(approx)
    
    # Bounding box measurements
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h if h != 0 else 0
    
    # Extent: ratio of contour area to bounding box area
    bbox_area = w * h
    extent = float(area) / bbox_area if bbox_area > 0 else 0
    
    # Convexity
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area if hull_area > 0 else 0
    
    # Fit an ellipse (need at least 5 points)
    if len(contour) >= 5:
        ellipse = cv2.fitEllipse(contour)
        ellipse_ratio = min(ellipse[1]) / max(ellipse[1]) if max(ellipse[1]) > 0 else 0
    else:
        ellipse_ratio = 0
    
    return {
        'area': area,
        'perimeter': perimeter,
        'circularity': circularity,
        'vertices': vertices,
        'aspect_ratio': aspect_ratio,
        'extent': extent,
        'solidity': solidity,
        'ellipse_ratio': ellipse_ratio
    }

def classify_shape_robust(features):
    """
    Classify shape using multiple features with decision rules
    Returns: ('shape_name', confidence_score)
    """
    if features is None:
        return ('unknown', 0.0)
    
    # Extract features
    circularity = features['circularity']
    vertices = features['vertices']
    aspect_ratio = features['aspect_ratio']
    extent = features['extent']
    solidity = features['solidity']
    ellipse_ratio = features['ellipse_ratio']
    
    # Scoring system for each shape
    circle_score = 0.0
    square_score = 0.0
    rectangle_score = 0.0
    triangle_score = 0.0
    
    # CIRCLE detection rules (IMPROVED)
    if circularity > 0.85:
        circle_score += 4.0  # Increased from 3.0
    elif circularity > 0.75:
        circle_score += 2.5  # Increased from 2.0
    elif circularity > 0.65:
        circle_score += 1.5  # Increased from 1.0
    
    if ellipse_ratio > 0.9:  # Nearly circular ellipse
        circle_score += 2.5  # Increased from 2.0
    
    if vertices > 8:  # Many vertices suggests smooth curve
        circle_score += 2.0  # Increased from 1.5
    elif vertices >= 6:  # 6-8 vertices could be a circle approximation
        circle_score += 1.5  # NEW: catch hexagon approximations
    
    if extent > 0.75:  # Fills its bounding box well
        circle_score += 1.5  # Increased from 1.0
    
    # SQUARE detection rules
    if vertices == 4:
        square_score += 2.0
        
    # More forgiving aspect ratio for squares
    if 0.90 <= aspect_ratio <= 1.10:  # Very close to 1:1
        square_score += 3.5
    elif 0.75 <= aspect_ratio <= 1.30:  # Still pretty square
        square_score += 2.5
    
    # If it has high circularity AND 4 vertices, boost square score
    if 0.75 <= circularity <= 0.85 and vertices == 4:
        square_score += 2.0
        
    if 0.55 <= extent <= 0.90:  # Squares typically have this extent
        square_score += 1.5
        
    if solidity > 0.95:  # Very solid/convex
        square_score += 1.5
    elif solidity > 0.9:
        square_score += 1.0
    
    # RECTANGLE detection rules
    if vertices == 4:
        rectangle_score += 2.0
        
    # Only boost rectangle score if aspect ratio is clearly NOT square-like
    if aspect_ratio < 0.70 or aspect_ratio > 1.35:  # Clearly rectangular
        rectangle_score += 3.5
    elif aspect_ratio < 0.75 or aspect_ratio > 1.30:  # Somewhat rectangular
        rectangle_score += 2.0
        
    if 0.55 <= extent <= 0.75:
        rectangle_score += 1.0
        
    if solidity > 0.9:
        rectangle_score += 0.5
    
    # TRIANGLE detection rules
    if vertices == 3:
        triangle_score += 4.0  # Strong indicator
        
    if 0.35 <= extent <= 0.55:  # Triangles have lower extent
        triangle_score += 2.0
        
    if 0.85 <= solidity <= 0.95:
        triangle_score += 1.0
        
    if 0.4 <= circularity <= 0.6:
        triangle_score += 1.0
    
    # Determine winner
    scores = {
        'circle': circle_score,
        'square': square_score,
        'rectangle': rectangle_score,
        'triangle': triangle_score
    }
    
    max_shape = max(scores, key=scores.get)
    max_score = scores[max_shape]
    
    # Calculate confidence (normalize to 0-1)
    total_score = sum(scores.values())
    confidence = max_score / total_score if total_score > 0 else 0.0
    
    # Minimum confidence threshold
    if max_score < 2.0:
        return ('unknown', confidence)
    
    return (max_shape, confidence)

# Create output image
output_image = bgr_image.copy()

# Detect and classify each colored object
detected_objects = []

for color_name, color_info in color_ranges.items():
    # Create mask for this color
    mask = cv2.inRange(hsv_image, color_info['lower'], color_info['upper'])
    
    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Filter small noise
        if area > 100:
            # Calculate features
            features = calculate_shape_features(contour)
            
            # Classify shape
            shape_type, confidence = classify_shape_robust(features)
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Draw bounding box
            cv2.rectangle(output_image, (x, y), (x + w, y + h), 
                         color_info['display_color'], 2)
            
            # Draw center point
            cv2.circle(output_image, (center_x, center_y), 5, 
                      color_info['display_color'], -1)
            
            # Create label with color, shape, and confidence
            label = f"{color_name.upper()} {shape_type.upper()} ({confidence*100:.0f}%)"
            
            # Draw label background
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(output_image, 
                         (x, y - label_size[1] - 10), 
                         (x + label_size[0], y),
                         color_info['display_color'], -1)
            
            # Draw label text
            cv2.putText(output_image, label, (x, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Store detection info
            detected_objects.append({
                'color': color_name,
                'shape': shape_type,
                'confidence': confidence,
                'position': (center_x, center_y),
                'bounding_box': (x, y, w, h),
                'features': features
            })
            
            # Print detailed info
            print(f"✓ Detected: {color_name} {shape_type}")
            print(f"  Confidence: {confidence*100:.1f}%")
            print(f"  Position: ({center_x}, {center_y})")
            print(f"  Features:")
            print(f"    - Circularity: {features['circularity']:.3f}")
            print(f"    - Vertices: {features['vertices']}")
            print(f"    - Aspect Ratio: {features['aspect_ratio']:.3f}")
            print(f"    - Extent: {features['extent']:.3f}")
            print(f"    - Solidity: {features['solidity']:.3f}")
            print()

print(f"Total objects detected: {len(detected_objects)}")
for obj in detected_objects:
    print(f"- {obj['color'].capitalize()} {obj['shape']} (confidence: {obj['confidence']*100:.1f}%)")

# Save results
cv2.imwrite('shape_recognition_improved.png', output_image)
print("\nAnnotated image saved as 'shape_recognition_improved.png'")

# Keep simulation running
print("\nSimulation running. Close window to exit.")
try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    print("Closing...")
    p.disconnect()