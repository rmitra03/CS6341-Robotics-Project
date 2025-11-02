import pybullet as p
import time
import numpy as np
import cv2
from PIL import Image

print("=" * 60)
print("COMPLETE SHAPE SORTING SYSTEM")
print("=" * 60)

# Start PyBullet
p.connect(p.GUI)
p.setGravity(0, 0, -9.81)

# Create floor
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(baseCollisionShapeIndex=floor_shape, basePosition=[0, 0, 0])

print("\n[1/5] Building sorting container...")

# ========== SORTING CONTAINER ==========
# Container dimensions
container_height = 0.1
wall_thickness = 0.02
container_size = 0.5

# Base of container
base_collision = p.createCollisionShape(p.GEOM_BOX, 
                                       halfExtents=[container_size/2, container_size/2, 0.01])
base_visual = p.createVisualShape(p.GEOM_BOX, 
                                 halfExtents=[container_size/2, container_size/2, 0.01],
                                 rgbaColor=[0.6, 0.6, 0.6, 1])
base = p.createMultiBody(baseMass=0,
                        baseCollisionShapeIndex=base_collision,
                        baseVisualShapeIndex=base_visual,
                        basePosition=[0, 0.3, 0.01])

# Left wall
left_wall_collision = p.createCollisionShape(p.GEOM_BOX,
                                            halfExtents=[wall_thickness/2, container_size/2, container_height/2])
left_wall_visual = p.createVisualShape(p.GEOM_BOX,
                                      halfExtents=[wall_thickness/2, container_size/2, container_height/2],
                                      rgbaColor=[0.8, 0.8, 0.8, 1])
left_wall = p.createMultiBody(baseMass=0,
                             baseCollisionShapeIndex=left_wall_collision,
                             baseVisualShapeIndex=left_wall_visual,
                             basePosition=[-container_size/2, 0.3, container_height/2 + 0.02])

# Right wall
right_wall_collision = p.createCollisionShape(p.GEOM_BOX,
                                             halfExtents=[wall_thickness/2, container_size/2, container_height/2])
right_wall_visual = p.createVisualShape(p.GEOM_BOX,
                                       halfExtents=[wall_thickness/2, container_size/2, container_height/2],
                                       rgbaColor=[0.8, 0.8, 0.8, 1])
right_wall = p.createMultiBody(baseMass=0,
                              baseCollisionShapeIndex=right_wall_collision,
                              baseVisualShapeIndex=right_wall_visual,
                              basePosition=[container_size/2, 0.3, container_height/2 + 0.02])

# Front wall
front_wall_collision = p.createCollisionShape(p.GEOM_BOX,
                                             halfExtents=[container_size/2, wall_thickness/2, container_height/2])
front_wall_visual = p.createVisualShape(p.GEOM_BOX,
                                       halfExtents=[container_size/2, wall_thickness/2, container_height/2],
                                       rgbaColor=[0.8, 0.8, 0.8, 1])
front_wall = p.createMultiBody(baseMass=0,
                              baseCollisionShapeIndex=front_wall_collision,
                              baseVisualShapeIndex=front_wall_visual,
                              basePosition=[0, 0.3 - container_size/2, container_height/2 + 0.02])

# Back wall
back_wall_collision = p.createCollisionShape(p.GEOM_BOX,
                                            halfExtents=[container_size/2, wall_thickness/2, container_height/2])
back_wall_visual = p.createVisualShape(p.GEOM_BOX,
                                      halfExtents=[container_size/2, wall_thickness/2, container_height/2],
                                      rgbaColor=[0.8, 0.8, 0.8, 1])
back_wall = p.createMultiBody(baseMass=0,
                             baseCollisionShapeIndex=back_wall_collision,
                             baseVisualShapeIndex=back_wall_visual,
                             basePosition=[0, 0.3 + container_size/2, container_height/2 + 0.02])

# Top panel with slots
slot_spacing = 0.15
panel_thickness = 0.01

# Strip 1: Far left
strip1_collision = p.createCollisionShape(p.GEOM_BOX,
                                         halfExtents=[0.08, container_size/2, panel_thickness])
strip1_visual = p.createVisualShape(p.GEOM_BOX,
                                   halfExtents=[0.08, container_size/2, panel_thickness],
                                   rgbaColor=[0.7, 0.7, 0.7, 1])
strip1 = p.createMultiBody(baseMass=0,
                          baseCollisionShapeIndex=strip1_collision,
                          baseVisualShapeIndex=strip1_visual,
                          basePosition=[-0.32, 0.3, container_height + 0.02])

# Strip 2: Between square and circle
strip2_collision = p.createCollisionShape(p.GEOM_BOX,
                                         halfExtents=[0.03, container_size/2, panel_thickness])
strip2_visual = p.createVisualShape(p.GEOM_BOX,
                                   halfExtents=[0.03, container_size/2, panel_thickness],
                                   rgbaColor=[0.7, 0.7, 0.7, 1])
strip2 = p.createMultiBody(baseMass=0,
                          baseCollisionShapeIndex=strip2_collision,
                          baseVisualShapeIndex=strip2_visual,
                          basePosition=[-0.075, 0.3, container_height + 0.02])

# Strip 3: Between circle and triangle
strip3_collision = p.createCollisionShape(p.GEOM_BOX,
                                         halfExtents=[0.03, container_size/2, panel_thickness])
strip3_visual = p.createVisualShape(p.GEOM_BOX,
                                   halfExtents=[0.03, container_size/2, panel_thickness],
                                   rgbaColor=[0.7, 0.7, 0.7, 1])
strip3 = p.createMultiBody(baseMass=0,
                          baseCollisionShapeIndex=strip3_collision,
                          baseVisualShapeIndex=strip3_visual,
                          basePosition=[0.075, 0.3, container_height + 0.02])

# Strip 4: Far right
strip4_collision = p.createCollisionShape(p.GEOM_BOX,
                                         halfExtents=[0.08, container_size/2, panel_thickness])
strip4_visual = p.createVisualShape(p.GEOM_BOX,
                                   halfExtents=[0.08, container_size/2, panel_thickness],
                                   rgbaColor=[0.7, 0.7, 0.7, 1])
strip4 = p.createMultiBody(baseMass=0,
                          baseCollisionShapeIndex=strip4_collision,
                          baseVisualShapeIndex=strip4_visual,
                          basePosition=[0.32, 0.3, container_height + 0.02])

# Visual markers for slots
square_marker_visual = p.createVisualShape(p.GEOM_BOX,
                                          halfExtents=[0.06, 0.06, 0.001],
                                          rgbaColor=[1, 0.3, 0.3, 0.8])
square_marker = p.createMultiBody(baseMass=0,
                                 baseVisualShapeIndex=square_marker_visual,
                                 basePosition=[-slot_spacing, 0.3, container_height + 0.025])

circle_marker_visual = p.createVisualShape(p.GEOM_CYLINDER,
                                          radius=0.055,
                                          length=0.001,
                                          rgbaColor=[0.3, 1, 0.3, 0.8])
circle_marker = p.createMultiBody(baseMass=0,
                                 baseVisualShapeIndex=circle_marker_visual,
                                 basePosition=[0, 0.3, container_height + 0.025])

triangle_marker_visual = p.createVisualShape(p.GEOM_BOX,
                                            halfExtents=[0.065, 0.045, 0.001],
                                            rgbaColor=[0.3, 0.3, 1, 0.8])
triangle_marker = p.createMultiBody(baseMass=0,
                                   baseVisualShapeIndex=triangle_marker_visual,
                                   basePosition=[slot_spacing, 0.3, container_height + 0.025])

print("✓ Sorting container built with 3 slots")

# ========== CREATE SHAPES TO SORT ==========
print("\n[2/5] Creating shapes...")

# Red square - positioned away from container
square_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025])
square_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025], 
                                    rgbaColor=[1, 0, 0, 1])
red_square = p.createMultiBody(baseMass=0.5,
                               baseCollisionShapeIndex=square_collision,
                               baseVisualShapeIndex=square_visual,
                               basePosition=[-0.15, -0.2, 0.5])

# Green circle
circle_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.05, height=0.05)
circle_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.05, length=0.05,
                                    rgbaColor=[0, 1, 0, 1])
green_circle = p.createMultiBody(baseMass=0.5,
                                 baseCollisionShapeIndex=circle_collision,
                                 baseVisualShapeIndex=circle_visual,
                                 basePosition=[0, -0.2, 0.5])

# Blue rectangle
rectangle_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025])
rectangle_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025],
                                      rgbaColor=[0, 0, 1, 1])
blue_rectangle = p.createMultiBody(baseMass=0.5,
                                  baseCollisionShapeIndex=rectangle_collision,
                                  baseVisualShapeIndex=rectangle_visual,
                                  basePosition=[0.15, -0.2, 0.5])

print("✓ Created 3 shapes: red square, green circle, blue rectangle")

# Let shapes settle
print("\n[3/5] Letting shapes settle...")
for i in range(200):
    p.stepSimulation()
    time.sleep(1./240.)
print("✓ Shapes settled")

# ========== CAMERA SETUP ==========
print("\n[4/5] Setting up camera and taking picture...")

camera_position = [0, -0.5, 0.6]
target_position = [0, -0.1, 0.05]
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

print("✓ Camera image captured")

# ========== SHAPE RECOGNITION ==========
print("\n[5/5] Running shape recognition...")

# Color ranges
color_ranges = {
    'red': {
        'lower': np.array([0, 100, 100]),
        'upper': np.array([10, 255, 255]),
        'display_color': (0, 0, 255),
        'shape_name': 'square'
    },
    'green': {
        'lower': np.array([40, 100, 100]),
        'upper': np.array([80, 255, 255]),
        'display_color': (0, 255, 0),
        'shape_name': 'circle'
    },
    'blue': {
        'lower': np.array([100, 100, 100]),
        'upper': np.array([130, 255, 255]),
        'display_color': (255, 0, 0),
        'shape_name': 'rectangle'
    }
}

def calculate_shape_features(contour):
    """Calculate geometric features for shape classification"""
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    
    if perimeter == 0:
        return None
    
    circularity = 4 * np.pi * area / (perimeter * perimeter)
    epsilon = 0.04 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)
    vertices = len(approx)
    
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h if h != 0 else 0
    bbox_area = w * h
    extent = float(area) / bbox_area if bbox_area > 0 else 0
    
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area if hull_area > 0 else 0
    
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
    """Classify shape using multiple features - TIGHTER THRESHOLDS"""
    if features is None:
        return ('unknown', 0.0)
    
    circularity = features['circularity']
    vertices = features['vertices']
    aspect_ratio = features['aspect_ratio']
    extent = features['extent']
    solidity = features['solidity']
    ellipse_ratio = features['ellipse_ratio']
    
    circle_score = 0.0
    square_score = 0.0
    rectangle_score = 0.0
    
    # Circle detection (STRONG)
    if circularity > 0.85:
        circle_score += 5.0
    elif circularity > 0.75:
        circle_score += 3.0
    elif circularity > 0.65:
        circle_score += 1.5
    
    if ellipse_ratio > 0.9:
        circle_score += 2.5
    
    if vertices > 8:
        circle_score += 2.5
    elif vertices >= 6:
        circle_score += 2.0
    
    if extent > 0.75:
        circle_score += 2.0
    
    # Square detection (TIGHT - must be close to 1:1)
    if vertices == 4:
        square_score += 2.5
        
    # Very tight aspect ratio requirements for squares
    if 0.92 <= aspect_ratio <= 1.08:  # Nearly perfect square
        square_score += 5.0
    elif 0.85 <= aspect_ratio <= 1.18:  # Still pretty square
        square_score += 3.0
    
    # Boost for high circularity + 4 vertices (square at angle)
    if 0.70 <= circularity <= 0.85 and vertices == 4:
        square_score += 2.5
        
    if 0.50 <= extent <= 0.92:
        square_score += 1.5
        
    if solidity > 0.95:
        square_score += 1.5
    elif solidity > 0.90:
        square_score += 1.0
    
    # Rectangle detection (must be clearly NOT square)
    if vertices == 4:
        rectangle_score += 2.0
        
    # Strong boost for clearly non-square ratios
    if aspect_ratio < 0.80 or aspect_ratio > 1.25:  # Clearly rectangular
        rectangle_score += 5.0
    elif aspect_ratio < 0.85 or aspect_ratio > 1.18:  # Moderately rectangular
        rectangle_score += 2.5
        
    if 0.55 <= extent <= 0.85:
        rectangle_score += 1.5
        
    if solidity > 0.9:
        rectangle_score += 1.0
    
    scores = {
        'circle': circle_score,
        'square': square_score,
        'rectangle': rectangle_score
    }
    
    max_shape = max(scores, key=scores.get)
    max_score = scores[max_shape]
    
    total_score = sum(scores.values())
    confidence = max_score / total_score if total_score > 0 else 0.0
    
    if max_score < 2.0:
        return ('unknown', confidence)
    
    return (max_shape, confidence)

# Create output image
output_image = bgr_image.copy()
detected_objects = []

for color_name, color_info in color_ranges.items():
    mask = cv2.inRange(hsv_image, color_info['lower'], color_info['upper'])
    
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 100:
            features = calculate_shape_features(contour)
            shape_type, confidence = classify_shape_robust(features)
            
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            
            cv2.rectangle(output_image, (x, y), (x + w, y + h), 
                         color_info['display_color'], 2)
            
            cv2.circle(output_image, (center_x, center_y), 5, 
                      color_info['display_color'], -1)
            
            label = f"{color_name.upper()} {shape_type.upper()} ({confidence*100:.0f}%)"
            
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(output_image, 
                         (x, y - label_size[1] - 10), 
                         (x + label_size[0], y),
                         color_info['display_color'], -1)
            
            cv2.putText(output_image, label, (x, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            detected_objects.append({
                'color': color_name,
                'shape': shape_type,
                'confidence': confidence,
                'position': (center_x, center_y),
                'expected_shape': color_info['shape_name']
            })

# Save annotated image
cv2.imwrite('complete_system_output.png', output_image)

print("\n" + "=" * 60)
print("DETECTION RESULTS")
print("=" * 60)

for obj in detected_objects:
    match = "✓ MATCH" if obj['shape'] == obj['expected_shape'] else "✗ MISMATCH"
    print(f"\n{obj['color'].upper()} object:")
    print(f"  Detected as: {obj['shape']}")
    print(f"  Expected: {obj['expected_shape']}")
    print(f"  Confidence: {obj['confidence']*100:.1f}%")
    print(f"  {match}")

accuracy = sum(1 for obj in detected_objects if obj['shape'] == obj['expected_shape']) / len(detected_objects) * 100
print(f"\n" + "=" * 60)
print(f"OVERALL ACCURACY: {accuracy:.1f}%")
print(f"Detected {len(detected_objects)}/3 objects")
print("=" * 60)

print("\n✓ Annotated image saved as 'complete_system_output.png'")
print("\n" + "=" * 60)
print("SYSTEM READY")
print("=" * 60)
print("\nThe complete sorting system is now running!")
print("- Sorting container with 3 slots (red=square, green=circle, blue=rectangle)")
print("- 3 colored shapes positioned for sorting")
print("- Camera capturing and analyzing shapes")
print("- Shape recognition identifying each object")
print("\nNext steps: Integrate robot arm for pick-and-place operations")
print("\nSimulation running. Close window to exit.")

# Keep simulation running
try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    print("\nShutting down...")
    p.disconnect()