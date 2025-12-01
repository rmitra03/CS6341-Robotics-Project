import pybullet as p
import time
import numpy as np

# Start PyBullet
p.connect(p.GUI)
p.setGravity(0, 0, -9.81)

# Create floor
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(baseCollisionShapeIndex=floor_shape, basePosition=[0, 0, 0])

print("Creating sorting container...")

# Sorting container
# We'll build it from multiple boxes to create a container with slots

# Container dimensions
container_height = 0.1
wall_thickness = 0.02
container_size = 0.5  # overall size

# Base of container (bottom panel)
base_collision = p.createCollisionShape(p.GEOM_BOX, 
                                       halfExtents=[container_size/2, container_size/2, 0.01])
base_visual = p.createVisualShape(p.GEOM_BOX, 
                                 halfExtents=[container_size/2, container_size/2, 0.01],
                                 rgbaColor=[0.6, 0.6, 0.6, 1])
base = p.createMultiBody(baseMass=0,  # Static (doesn't move)
                        baseCollisionShapeIndex=base_collision,
                        baseVisualShapeIndex=base_visual,
                        basePosition=[0, 0, 0.01])

# Left wall
left_wall_collision = p.createCollisionShape(p.GEOM_BOX,
                                            halfExtents=[wall_thickness/2, container_size/2, container_height/2])
left_wall_visual = p.createVisualShape(p.GEOM_BOX,
                                      halfExtents=[wall_thickness/2, container_size/2, container_height/2],
                                      rgbaColor=[0.8, 0.8, 0.8, 1])
left_wall = p.createMultiBody(baseMass=0,
                             baseCollisionShapeIndex=left_wall_collision,
                             baseVisualShapeIndex=left_wall_visual,
                             basePosition=[-container_size/2, 0, container_height/2 + 0.02])

# Right wall
right_wall_collision = p.createCollisionShape(p.GEOM_BOX,
                                             halfExtents=[wall_thickness/2, container_size/2, container_height/2])
right_wall_visual = p.createVisualShape(p.GEOM_BOX,
                                       halfExtents=[wall_thickness/2, container_size/2, container_height/2],
                                       rgbaColor=[0.8, 0.8, 0.8, 1])
right_wall = p.createMultiBody(baseMass=0,
                              baseCollisionShapeIndex=right_wall_collision,
                              baseVisualShapeIndex=right_wall_visual,
                              basePosition=[container_size/2, 0, container_height/2 + 0.02])

# Front wall
front_wall_collision = p.createCollisionShape(p.GEOM_BOX,
                                             halfExtents=[container_size/2, wall_thickness/2, container_height/2])
front_wall_visual = p.createVisualShape(p.GEOM_BOX,
                                       halfExtents=[container_size/2, wall_thickness/2, container_height/2],
                                       rgbaColor=[0.8, 0.8, 0.8, 1])
front_wall = p.createMultiBody(baseMass=0,
                              baseCollisionShapeIndex=front_wall_collision,
                              baseVisualShapeIndex=front_wall_visual,
                              basePosition=[0, -container_size/2, container_height/2 + 0.02])

# Back wall
back_wall_collision = p.createCollisionShape(p.GEOM_BOX,
                                            halfExtents=[container_size/2, wall_thickness/2, container_height/2])
back_wall_visual = p.createVisualShape(p.GEOM_BOX,
                                      halfExtents=[container_size/2, wall_thickness/2, container_height/2],
                                      rgbaColor=[0.8, 0.8, 0.8, 1])
back_wall = p.createMultiBody(baseMass=0,
                             baseCollisionShapeIndex=back_wall_collision,
                             baseVisualShapeIndex=back_wall_visual,
                             basePosition=[0, container_size/2, container_height/2 + 0.02])

# Top panel with slots
# This is the tricky part - we'll create a panel with holes

# We'll use a compound shape (multiple shapes combined)
# Create sections of the top panel with gaps for slots

slot_spacing = 0.15  # Space between slots
panel_thickness = 0.01

# Top panel positions for slots (left to right: square, circle, triangle)
slot_positions = [
    (-slot_spacing, 0),   # Square slot position
    (0, 0),               # Circle slot position  
    (slot_spacing, 0)     # Triangle slot position
]

# Create top panel sections around the slots
# We'll make 4 strips that leave gaps for the slots

# Strip 1: Far left
strip1_collision = p.createCollisionShape(p.GEOM_BOX,
                                         halfExtents=[0.08, container_size/2, panel_thickness])
strip1_visual = p.createVisualShape(p.GEOM_BOX,
                                   halfExtents=[0.08, container_size/2, panel_thickness],
                                   rgbaColor=[0.7, 0.7, 0.7, 1])
strip1 = p.createMultiBody(baseMass=0,
                          baseCollisionShapeIndex=strip1_collision,
                          baseVisualShapeIndex=strip1_visual,
                          basePosition=[-0.32, 0, container_height + 0.02])

# Strip 2: Between square and circle
strip2_collision = p.createCollisionShape(p.GEOM_BOX,
                                         halfExtents=[0.03, container_size/2, panel_thickness])
strip2_visual = p.createVisualShape(p.GEOM_BOX,
                                   halfExtents=[0.03, container_size/2, panel_thickness],
                                   rgbaColor=[0.7, 0.7, 0.7, 1])
strip2 = p.createMultiBody(baseMass=0,
                          baseCollisionShapeIndex=strip2_collision,
                          baseVisualShapeIndex=strip2_visual,
                          basePosition=[-0.075, 0, container_height + 0.02])

# Strip 3: Between circle and triangle
strip3_collision = p.createCollisionShape(p.GEOM_BOX,
                                         halfExtents=[0.03, container_size/2, panel_thickness])
strip3_visual = p.createVisualShape(p.GEOM_BOX,
                                   halfExtents=[0.03, container_size/2, panel_thickness],
                                   rgbaColor=[0.7, 0.7, 0.7, 1])
strip3 = p.createMultiBody(baseMass=0,
                          baseCollisionShapeIndex=strip3_collision,
                          baseVisualShapeIndex=strip3_visual,
                          basePosition=[0.075, 0, container_height + 0.02])

# Strip 4: Far right
strip4_collision = p.createCollisionShape(p.GEOM_BOX,
                                         halfExtents=[0.08, container_size/2, panel_thickness])
strip4_visual = p.createVisualShape(p.GEOM_BOX,
                                   halfExtents=[0.08, container_size/2, panel_thickness],
                                   rgbaColor=[0.7, 0.7, 0.7, 1])
strip4 = p.createMultiBody(baseMass=0,
                          baseCollisionShapeIndex=strip4_collision,
                          baseVisualShapeIndex=strip4_visual,
                          basePosition=[0.32, 0, container_height + 0.02])

# Add visual markers for slots (colored rectangles to show where each slot is)
# Red marker for square slot
square_marker_visual = p.createVisualShape(p.GEOM_BOX,
                                          halfExtents=[0.06, 0.06, 0.001],
                                          rgbaColor=[1, 0.3, 0.3, 0.8])
square_marker = p.createMultiBody(baseMass=0,
                                 baseVisualShapeIndex=square_marker_visual,
                                 basePosition=[-slot_spacing, 0, container_height + 0.025])

# Green marker for circle slot
circle_marker_visual = p.createVisualShape(p.GEOM_CYLINDER,
                                          radius=0.055,
                                          length=0.001,
                                          rgbaColor=[0.3, 1, 0.3, 0.8])
circle_marker = p.createMultiBody(baseMass=0,
                                 baseVisualShapeIndex=circle_marker_visual,
                                 basePosition=[0, 0, container_height + 0.025])

# Blue marker for triangle slot
triangle_marker_visual = p.createVisualShape(p.GEOM_BOX,
                                            halfExtents=[0.065, 0.045, 0.001],
                                            rgbaColor=[0.3, 0.3, 1, 0.8])
triangle_marker = p.createMultiBody(baseMass=0,
                                   baseVisualShapeIndex=triangle_marker_visual,
                                   basePosition=[slot_spacing, 0, container_height + 0.025])

print("Container created with 3 slots!")

# Create some shapes to sort
print("\nCreating shapes to sort...")

# Red square - positioned above the container (HEAVIER NOW)
square_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025])
square_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025], 
                                    rgbaColor=[1, 0, 0, 1])
red_square = p.createMultiBody(baseMass=2.0,  # Increased from 0.1 to 2.0
                               baseCollisionShapeIndex=square_collision,
                               baseVisualShapeIndex=square_visual,
                               basePosition=[-slot_spacing, -0.3, 0.3])
# Add damping to reduce floatiness
p.changeDynamics(red_square, -1, linearDamping=0.9, angularDamping=0.9)

# Green circle (HEAVIER NOW)
circle_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.05, height=0.05)
circle_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.05, length=0.05,
                                    rgbaColor=[0, 1, 0, 1])
green_circle = p.createMultiBody(baseMass=2.0,  # Increased from 0.1 to 2.0
                                 baseCollisionShapeIndex=circle_collision,
                                 baseVisualShapeIndex=circle_visual,
                                 basePosition=[0, -0.3, 0.3])
# Add damping to reduce floatiness
p.changeDynamics(green_circle, -1, linearDamping=0.9, angularDamping=0.9)

# Blue triangle (HEAVIER NOW)
triangle_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025])
triangle_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025],
                                      rgbaColor=[0, 0, 1, 1])
blue_triangle = p.createMultiBody(baseMass=2.0,  # Increased from 0.1 to 2.0
                                  baseCollisionShapeIndex=triangle_collision,
                                  baseVisualShapeIndex=triangle_visual,
                                  basePosition=[slot_spacing, -0.3, 0.3])
# Add damping to reduce floatiness
p.changeDynamics(blue_triangle, -1, linearDamping=0.9, angularDamping=0.9)

print("The shapes are positioned above the container.")
print("Try manually dropping them into the slots!")
print("- Red square goes in the red (left) slot")
print("- Green circle goes in the green (middle) slot")
print("- Blue triangle goes in the blue (right) slot")
print("\nYou can click and drag shapes with your mouse in the simulation.")
print("Hold Ctrl (Cmd on Mac) while dragging to move objects.")
print("Close window to exit.\n")

# Run simulation
try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    print("Closing...")
    p.disconnect()