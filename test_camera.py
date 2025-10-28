import pybullet as p
import time
import numpy as np
from PIL import Image

# Start PyBullet
p.connect(p.GUI)
p.setGravity(0, 0, -9.81)

# Create floor
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(baseCollisionShapeIndex=floor_shape, basePosition=[0, 0, 0])

# Create some shapes to look at
print("Creating shapes...")

# Red square
square_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025])
square_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025], 
                                    rgbaColor=[1, 0, 0, 1])
red_square = p.createMultiBody(baseMass=0.1,
                               baseCollisionShapeIndex=square_collision,
                               baseVisualShapeIndex=square_visual,
                               basePosition=[0, 0, 0.5])

# Green circle
circle_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.05, height=0.05)
circle_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.05, length=0.05,
                                    rgbaColor=[0, 1, 0, 1])
green_circle = p.createMultiBody(baseMass=0.1,
                                 baseCollisionShapeIndex=circle_collision,
                                 baseVisualShapeIndex=circle_visual,
                                 basePosition=[0.2, 0, 0.5])

# Blue triangle (box for now)
triangle_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025])
triangle_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025],
                                      rgbaColor=[0, 0, 1, 1])
blue_triangle = p.createMultiBody(baseMass=0.1,
                                  baseCollisionShapeIndex=triangle_collision,
                                  baseVisualShapeIndex=triangle_visual,
                                  basePosition=[0.4, 0, 0.5])

# Let shapes settle
print("Letting shapes settle...")
for i in range(200):
    p.stepSimulation()
    time.sleep(1./240.)

# ========== CAMERA SETUP ==========

# Camera position and orientation
camera_position = [0.2, -0.5, 0.5]  # x, y, z position
target_position = [0.2, 0, 0.05]     # where camera looks at
up_vector = [0, 0, 1]                # which way is "up"

# Camera settings
width = 640   # image width in pixels
height = 480  # image height in pixels
fov = 60      # field of view in degrees
aspect = width / height
near = 0.1    # near clipping plane
far = 3.0     # far clipping plane

# Calculate view matrix (where camera is looking from)
view_matrix = p.computeViewMatrix(
    cameraEyePosition=camera_position,
    cameraTargetPosition=target_position,
    cameraUpVector=up_vector
)

# Calculate projection matrix (camera lens properties)
projection_matrix = p.computeProjectionMatrixFOV(
    fov=fov,
    aspect=aspect,
    nearVal=near,
    farVal=far
)

# Take a picture!
print("Taking picture...")
img_data = p.getCameraImage(
    width=width,
    height=height,
    viewMatrix=view_matrix,
    projectionMatrix=projection_matrix,
    renderer=p.ER_BULLET_HARDWARE_OPENGL  # Use hardware rendering
)

# Extract the RGB image from the data
# img_data returns: width, height, rgb_array, depth_array, segmentation_mask
rgb_array = img_data[2]  # This is the color image
width = img_data[0]
height = img_data[1]

# Convert to numpy array and reshape
rgb_array = np.array(rgb_array, dtype=np.uint8)
rgb_array = rgb_array.reshape((height, width, 4))  # RGBA format

# Remove alpha channel (we just want RGB)
rgb_array = rgb_array[:, :, :3]

# Save the image
img = Image.fromarray(rgb_array)
img.save("camera_view.png")
print("Image saved as 'camera_view.png'!")

# Show some info
print(f"Image size: {width}x{height}")
print(f"Camera position: {camera_position}")
print(f"Looking at: {target_position}")

# Keep simulation running so you can see the setup
print("\nSimulation running. Close window to exit.")
try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    print("Closing...")
    p.disconnect()