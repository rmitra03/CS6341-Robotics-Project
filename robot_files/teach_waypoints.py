"""
teach_waypoints.py
Record robot positions for teach-and-replay sorting

USAGE:
1. Run this script
2. Manually move the SO-101 arm to each position when prompted
3. Press Enter to record each position
4. Waypoints are saved to 'sorting_waypoints.json'
"""

from lerobot.robots.so101_follower import SO101Follower, SO101FollowerConfig
import json
import time

# Configuration
PORT = "COM4"  # Change this to match your setup
ROBOT_ID = "my_awesome_follower_arm"

# Waypoint definitions
# These are the positions needed to be recorded for sorting
waypoint_names = [
    # Starting position
    "home",
    
    # Position 1 (e.g., where red square will be)
    "approach_pos1",  # Above the shape
    "grasp_pos1",     # Down at shape level
    "lift_pos1",      # Lifted with shape
    
    # Position 2 (e.g., where green circle will be)
    "approach_pos2",
    "grasp_pos2",
    "lift_pos2",
    
    # Position 3 (e.g., where blue rectangle will be)
    "approach_pos3",
    "grasp_pos3",
    "lift_pos3",
    
    # Drop-off locations (sorting slots)
    "drop_red",       # Above red slot
    "drop_green",     # Above green slot
    "drop_blue",      # Above blue slot
]

# Main teaching function
def teach_waypoints():
    """Record waypoints by manually positioning the robot"""

    print("TEACH MODE - SO-101 Waypoint Recording")
    print("\nInstructions:")
    print("1. Manually move the robot arm to each position")
    print("2. Press Enter to record that position")
    print("3. Repeat for all positions")
    print("\nNote: You can physically move the arm if it's in compliance mode,")
    print("or use a teaching pendant/joystick if available.")
    
    # Connect to robot
    print("\nConnecting to SO-101...")
    robot_config = SO101FollowerConfig(port=PORT, id=ROBOT_ID)
    robot = SO101Follower(robot_config)
    robot.connect()
    print("Connected!")
    
    waypoints = {}
    
    try:
        for i, waypoint_name in enumerate(waypoint_names, 1):
            print(f"\n[{i}/{len(waypoint_names)}] {waypoint_name}")
            print("-" * 40)
            
            # Give instructions for specific waypoints
            if "home" in waypoint_name:
                print("Move robot to safe HOME position (center, raised)")
            elif "approach" in waypoint_name:
                print("Move gripper ABOVE the pickup location")
            elif "grasp" in waypoint_name:
                print("Move gripper DOWN to grasp height (but don't close yet)")
            elif "lift" in waypoint_name:
                print("Move gripper UP to safe carry height")
            elif "drop" in waypoint_name:
                print("Move gripper ABOVE the sorting slot")
            
            input("Press Enter when ready to record...")
            
            # Read current position
            obs = robot.get_observation()
            
            # Store all joint positions
            waypoints[waypoint_name] = {
                'shoulder_pan.pos': obs['shoulder_pan.pos'],
                'shoulder_lift.pos': obs['shoulder_lift.pos'],
                'elbow_flex.pos': obs['elbow_flex.pos'],
                'wrist_flex.pos': obs['wrist_flex.pos'],
                'wrist_roll.pos': obs['wrist_roll.pos'],
                'gripper.pos': obs['gripper.pos'],
            }
            
            # Display recorded values
            print(f"Recorded '{waypoint_name}':")
            for joint, value in waypoints[waypoint_name].items():
                print(f"  {joint}: {value:.2f}")
        
        # Save to file
        print("\n" + "-" * 40)
        print("Saving waypoints to file...")
        with open('sorting_waypoints.json', 'w') as f:
            json.dump(waypoints, f, indent=2)
        
        print("Waypoints saved to 'sorting_waypoints.json'")
        print(f"\nTotal waypoints recorded: {len(waypoints)}")
        print("\nYou can now use these waypoints with the sorting controller!")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("\nDisconnecting...")
        robot.disconnect()
        print("Done!")

# Main function
if __name__ == "__main__":
    teach_waypoints()