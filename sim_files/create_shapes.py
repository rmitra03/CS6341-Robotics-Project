import pybullet as p
import time

# Start PyBullet with a window you can see
p.connect(p.GUI)

# Add gravity (makes things fall down naturally)
p.setGravity(0, 0, -9.81)

# Create a floor so shapes don't fall forever
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(baseCollisionShapeIndex=floor_shape, basePosition=[0, 0, 0])

# RED SQUARE
print("Creating red square...")
square_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025])
square_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.025], 
                                    rgbaColor=[1, 0, 0, 1])
red_square = p.createMultiBody(baseMass=0.1,
                               baseCollisionShapeIndex=square_collision,
                               baseVisualShapeIndex=square_visual,
                               basePosition=[0, 0, 1.0])

# GREEN CIRCLE
print("Creating green circle...")
circle_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.05, height=0.05)
circle_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.05, length=0.05,
                                    rgbaColor=[0, 1, 0, 1])
green_circle = p.createMultiBody(baseMass=0.1,
                                 baseCollisionShapeIndex=circle_collision,
                                 baseVisualShapeIndex=circle_visual,
                                 basePosition=[0.3, 0, 1.0])

# BLUE TRIANGLE (simplified as a box for now)
print("Creating blue triangle...")
triangle_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025])
triangle_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.06, 0.04, 0.025],
                                      rgbaColor=[0, 0, 1, 1])
blue_triangle = p.createMultiBody(baseMass=0.1,
                                  baseCollisionShapeIndex=triangle_collision,
                                  baseVisualShapeIndex=triangle_visual,
                                  basePosition=[0.6, 0, 1.0])

# YELLOW STAR
print("Creating yellow star...")
star_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.055, 0.055, 0.025])
star_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.055, 0.055, 0.025],
                                  rgbaColor=[1, 1, 0, 1])
yellow_star = p.createMultiBody(baseMass=0.1,
                                baseCollisionShapeIndex=star_collision,
                                baseVisualShapeIndex=star_visual,
                                basePosition=[-0.3, 0, 1.0])

print("All shapes created!")

# Run the physics simulation
for i in range(500):
    p.stepSimulation()
    time.sleep(1./240.)

print("Simulation running... Close the window or press Ctrl+C to exit.")

# Keep the window open until you close it
try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    print("Closing simulation...")
    p.disconnect()