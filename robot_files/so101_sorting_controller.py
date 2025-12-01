"""
so101_sorting_controller.py
Complete sorting system integrating:
- Real camera color detection
- SO-101 robot arm control
- Teach-and-replay execution

USAGE:
1. First run teach_waypoints.py to record positions
2. Place colored shapes at the recorded positions
3. Run this script to execute sorting
"""

from lerobot.robots.so101_follower import SO101Follower, SO101FollowerConfig
import cv2
import numpy as np
import json
import time

# Configuration
PORT = "COM4"  # Change to match your setup
ROBOT_ID = "my_awesome_follower_arm"
WAYPOINTS_FILE = "sorting_waypoints.json"

# Camera settings
CAMERA_ID = 0  # Try 0, 1, or 2 if this doesn't work
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Gripper positions (adjust these based on your gripper)
GRIPPER_OPEN = 0.0
GRIPPER_CLOSED = 50.0

# COLOR DETECTION (from detect_colors.py)
def detect_colored_objects(frame):
    """
    Detect colored objects in a camera frame
    Returns list of detected objects with their colors and positions
    """
    # Convert to HSV
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Color ranges (from original code)
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
    
    detected_objects = []
    
    for color_name, color_info in color_ranges.items():
        # Create mask
        mask = cv2.inRange(hsv_image, color_info['lower'], color_info['upper'])
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter small noise
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                center_x = x + w // 2
                center_y = y + h // 2
                
                detected_objects.append({
                    'color': color_name,
                    'position': (center_x, center_y),
                    'bounding_box': (x, y, w, h),
                    'area': area
                })
    
    return detected_objects

# Sorting controller class
class SO101SortingController:
    """Controls SO-101 robot arm for color-based sorting"""
    
    def __init__(self, robot, waypoints_file, camera_id=0):
        self.robot = robot
        
        # Load waypoints
        print(f"Loading waypoints from {waypoints_file}...")
        with open(waypoints_file, 'r') as f:
            self.waypoints = json.load(f)
        print(f"✓ Loaded {len(self.waypoints)} waypoints")
        
        # Initialize camera
        print(f"Initializing camera {camera_id}...")
        self.camera = cv2.VideoCapture(camera_id)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        time.sleep(2)  # Let camera warm up
        print("✓ Camera ready")
    
    def capture_and_detect(self):
        """Capture image and detect colored objects"""
        ret, frame = self.camera.read()
        if not ret:
            print("ERROR: Could not read from camera!")
            return None, []
        
        detected = detect_colored_objects(frame)
        return frame, detected
    
    def move_to_waypoint(self, waypoint_name, wait_time=2.0):
        """Move robot to a recorded waypoint"""
        if waypoint_name not in self.waypoints:
            print(f"ERROR: Waypoint '{waypoint_name}' not found!")
            return False
        
        print(f"  Moving to {waypoint_name}...")
        self.robot.send_action(self.waypoints[waypoint_name])
        time.sleep(wait_time)
        return True
    
    def set_gripper(self, position, wait_time=1.0):
        """Set gripper to specified position"""
        obs = self.robot.get_observation()
        action = {k: obs[k] for k in obs}
        action['gripper.pos'] = position
        self.robot.send_action(action)
        time.sleep(wait_time)
    
    def open_gripper(self):
        """Open the gripper"""
        print("  Opening gripper...")
        self.set_gripper(GRIPPER_OPEN)
    
    def close_gripper(self):
        """Close the gripper"""
        print("  Closing gripper...")
        self.set_gripper(GRIPPER_CLOSED)
    
    def pick_and_place(self, position_num, color):
        """
        Execute pick-and-place sequence
        
        Args:
            position_num: Which pickup position (1, 2, or 3)
            color: Color of object (determines drop location)
        """
        print(f"\n{'='*50}")
        print(f"Picking {color.upper()} object from position {position_num}")
        print('='*50)
        
        # 1. Approach
        self.move_to_waypoint(f"approach_pos{position_num}")
        
        # 2. Move down to grasp
        self.move_to_waypoint(f"grasp_pos{position_num}")
        
        # 3. Close gripper
        self.close_gripper()
        
        # 4. Lift
        self.move_to_waypoint(f"lift_pos{position_num}")
        
        # 5. Move to drop location
        self.move_to_waypoint(f"drop_{color}")
        
        # 6. Open gripper
        self.open_gripper()
        
        # 7. Return home
        self.move_to_waypoint("home")
        
        print(f"✓ {color.upper()} object sorted!\n")
    
    def run_sorting_simple(self):
        """
        Simple sorting routine:
        - Checks 3 fixed positions for colored objects
        - Executes pick-and-place for each detected object
        """
        print("STARTING SORTING SEQUENCE")
        
        # Move to home position
        print("\nMoving to home position...")
        self.move_to_waypoint("home")
        
        # Check each position
        positions_to_check = [1, 2, 3]
        
        for pos_num in positions_to_check:
            print(f"\n--- Checking Position {pos_num} ---")
            
            # Capture image and detect colors
            frame, detected = self.capture_and_detect()
            
            if detected:
                # For simplicity, take the first detected color
                # In a real system, you might use position to determine which object
                obj = detected[0]
                color = obj['color']
                
                print(f"Detected {color.upper()} object")
                print(f"Position: {obj['position']}")
                print(f"Area: {obj['area']} pixels")
                
                # Execute pick and place
                self.pick_and_place(pos_num, color)
            else:
                print(f"  No object detected at position {pos_num}")
        
        print("SORTING COMPLETE!")
    
    def run_sorting_vision_guided(self):
        """
        Vision-guided sorting:
        - Takes one image
        - Detects all colored objects
        - Sorts them based on detected positions
        
        NOTE: This requires camera calibration to map pixel positions
        to robot positions. Use run_sorting_simple() instead if camera calibration
        is not available.
        """
        print("\nVision-guided sorting not yet implemented.")
        print("Use run_sorting_simple() with fixed positions instead.")
    
    def cleanup(self):
        """Clean up resources"""
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()

# Main function
def main():
    print("SO-101 COLOR-BASED SORTING SYSTEM")
    
    # Initialize robot
    print("\nConnecting to SO-101...")
    robot_config = SO101FollowerConfig(port=PORT, id=ROBOT_ID)
    robot = SO101Follower(robot_config)
    robot.connect()
    print("Robot connected!")
    
    try:
        # Initialize controller
        controller = SO101SortingController(
            robot=robot,
            waypoints_file=WAYPOINTS_FILE,
            camera_id=CAMERA_ID
        )
        
        # Wait for user to start
        print("Setup complete!")
        print("Make sure colored shapes are placed at positions 1, 2, 3")
        input("Press Enter to start sorting...")
        
        # Run sorting
        controller.run_sorting_simple()
        
        print("\nAll done!")
        
    except FileNotFoundError:
        print(f"\nERROR: Could not find '{WAYPOINTS_FILE}'")
        print("Please run teach_waypoints.py first to record positions!")
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.cleanup()
        robot.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    main()