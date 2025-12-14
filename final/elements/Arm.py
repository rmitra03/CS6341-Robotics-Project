from lerobot.robots.so101_follower import SO101Follower, SO101FollowerConfig
import time
import json

class Arm:
    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.robot = None
        self.pose_file = "poses.json"
        self.safe_shoulder_norm = -40.0
        self.poses = {}

    def connect(self):
        cfg = SO101FollowerConfig(
            port=self.port,
            id="my_robot",
            disable_torque_on_disconnect=True,
            max_relative_target=None,
        )

        self.robot = SO101Follower(cfg)
        self.robot.connect()

        for joint, motor in self.robot.bus.motors.items():
            self.robot.bus._write(46, 2, motor.id, 900)

        print("CONNECTED")

    def disconnect(self):
        if self.robot:
            self.robot.disconnect()
            print("DISCONNECTED")
            self.robot = None

    def unlock(self):
        for joint in self.robot.bus.motors.keys():
            self.robot.bus.write("Torque_Enable", joint, 0)
        print("UNLOCKED (free movement)")

    def lock(self):
        for joint in self.robot.bus.motors.keys():
            self.robot.bus.write("Torque_Enable", joint, 1)
        print("LOCKED (motors active)")

    def move_shoulder_to_safe(self):
        if not self.robot:
            print("Robot not connected!")
            return

        action = {"shoulder_lift.pos": self.safe_shoulder_norm}
        print(f"Sending SAFE SHOULDER ACTION: {action}")

        self.robot.send_action(action)
        time.sleep(0.5)

        feedback = self.robot.bus.sync_read("Present_Position")
        sl = feedback.get("shoulder_lift", None)

        print(f"Feedback – shoulder_lift is now at: {sl}")

    def printPose(self):
        if self.robot is None:
            print("Not Connected")
            return

        pose = self.robot.bus.sync_read("Present_Position")

        for joint, val in pose.items():
            print(f"{joint:15s}: {val:8.2f}")

        return pose

    def printPoses(self):
        if self.robot is None:
            print("Not Connected")
            return

        for pose in self.poses:
            print(pose)

    def loadPoses(self):
        try:
            with open(self.pose_file, "r") as f:
                self.poses = json.load(f)
            print("Loaded poses from file.")
        except FileNotFoundError:
            print("No poses.json file found — starting with empty pose list.")
            self.poses = {}
        except json.JSONDecodeError:
            print("poses.json is corrupted — starting fresh.")
            self.poses = {}

    def learnPose(self, name):
        pose = self.robot.bus.sync_read("Present_Position")
        self.poses[name] = pose
        print(f"Pose '{name}' learned.")

    def savePoses(self):
        try:
            with open(self.pose_file, "r") as f:
                existing = json.load(f)
        except FileNotFoundError:
            existing = {}

        existing.update(self.poses)

        with open(self.pose_file, "w") as f:
            json.dump(existing, f, indent=2)

        print("Saved poses to file:", self.pose_file)

    def executePose(self, name):

        self.lock()
        if name not in self.poses:
            print(f"Pose '{name}' not found")
            return

        pose = self.poses[name]

        safe = self.safe_shoulder_norm
        self.robot.send_action({"shoulder_lift.pos": safe})
        time.sleep(1.0)

        phaseB = {}
        for joint, norm in pose.items():
            if joint in ["shoulder_lift", "gripper"]:
                continue
            phaseB[f"{joint}.pos"] = norm

        if phaseB:
            self.robot.send_action(phaseB)
            time.sleep(1.0)

        final_sl = pose["shoulder_lift"]
        self.robot.send_action({"shoulder_lift.pos": final_sl})
        time.sleep(1.0)

        if "gripper" in pose:
            grip = pose["gripper"]
            #self.robot.send_action({"gripper.pos": grip})
            time.sleep(1.0)

        print(f"Pose '{name}' Executed!")

    def Grip(self, value):
        if value > 90:
            return
        if value < -90:
            return

        self.robot.send_action({"gripper.pos": value})
        time.sleep(1.0)
