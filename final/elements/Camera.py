import cv2
import numpy as np


# ===========================
# HSV COLOR RANGES (TUNABLE)
# ===========================
BLUE_LOWER  = np.array([85, 50, 20])
BLUE_UPPER  = np.array([135, 255, 255])

GREEN_LOWER = np.array([40, 70, 40])
GREEN_UPPER = np.array([80, 255, 255])

# Red requires 2 HSV ranges
RED_LOWER1 = np.array([0, 100, 100])
RED_UPPER1 = np.array([10, 255, 255])
RED_LOWER2 = np.array([170, 100, 100])
RED_UPPER2 = np.array([180, 255, 255])


class Camera:
    def __init__(self, index=0):
        self.index = index
        self.cap = None


    # ===========================
    # CONNECT CAMERA
    # ===========================
    def connect(self):
        print(f"Connecting to camera index {self.index}...")
        self.cap = cv2.VideoCapture(self.index)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera!")

        # YUYV first
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))

        # White balance OFF
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0)

        # Auto exposure ON, then manual exposure value
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, -6)

        # MJPG final encoding
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

        print("Camera Connected!")


    # ===========================
    # DISCONNECT CAMERA
    # ===========================
    def disconnect(self):
        if self.cap:
            self.cap.release()
        self.cap = None
        print("Camera Disconnected!")


    # ===========================
    # DRAW GRID LINES
    # ===========================
    def addLine(self, frame, orientation, pixel, tilt_deg=0, color=(0, 0, 0), thickness=2):
        h, w = frame.shape[:2]

        # Support tilt expressed as string "5*"
        if isinstance(tilt_deg, str) and tilt_deg.endswith("*"):
            tilt = float(tilt_deg[:-1])
        else:
            tilt = float(tilt_deg)

        if orientation.lower().startswith("v"):
            x = int(pixel)
            pt1 = (x, 0)
            pt2 = (x + int(tilt), h)
            cv2.line(frame, pt1, pt2, color, thickness)
            return frame

        elif orientation.lower().startswith("h"):
            y = int(pixel)
            pt1 = (0, y)
            pt2 = (w, y + int(tilt))
            cv2.line(frame, pt1, pt2, color, thickness)
            return frame

        else:
            raise ValueError("orientation must be 'Vertical' or 'Horizontal'")


    # ===========================
    # COLOR DETECTION HELPERS
    # ===========================
    def _centroid_from_mask(self, mask):
        ys, xs = np.where(mask > 0)

        minimum = 100

        if len(xs) < minimum:
            return None

        return (int(np.mean(xs)), int(np.mean(ys)))  # (cx, cy)


    def detect_colors(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        colors = {}

        # BLUE
        mask_blue = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)
        c_blue = self._centroid_from_mask(mask_blue)
        if c_blue:
            colors["blue"] = c_blue

        # GREEN
        mask_green = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
        c_green = self._centroid_from_mask(mask_green)
        if c_green:
            colors["green"] = c_green

        # RED
        mask_red1 = cv2.inRange(hsv, RED_LOWER1, RED_UPPER1)
        mask_red2 = cv2.inRange(hsv, RED_LOWER2, RED_UPPER2)
        mask_red = mask_red1 | mask_red2
        c_red = self._centroid_from_mask(mask_red)
        if c_red:
            colors["red"] = c_red

        return colors


    def draw_centroids(self, frame, colors):
        for color, (cx, cy) in colors.items():
            # Dot
            cv2.circle(frame, (cx, cy), 6, (0, 0, 0), -1)
            # Label
            cv2.putText(
                frame, color, (cx + 8, cy - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 0, 0), 2
            )
        return frame

    def boost_saturation(self, frame, factor=1.3):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[..., 1] *= factor               # multiply saturation channel
        hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


    # ===========================
    # SNAPSHOT (GRID + COLOR CENTROIDS)
    # ===========================
    def snapshot(self, filename="capture.png"):

        # Warm-up frames
        for _ in range(10):
            ret, frame = self.cap.read()

        if not ret:
            raise RuntimeError("Failed to read frame")

        #frame = self.boost_saturation(frame, 1.5)
        #frame = self.boost_saturation(frame, 2)

        # Draw grid lines
        frame = self.addLine(frame, "Vertical", 260, "-35")
        frame = self.addLine(frame, "Vertical", 380, "35")
        frame = self.addLine(frame, "Horizontal", 165, "0")
        frame = self.addLine(frame, "Horizontal", 295, "0")

        # Detect colors
        colors = self.detect_colors(frame)

        for color, centroid in colors.items():
            print(color)
            print(centroid)
            if centroid is None:
                continue

            cx, cy = centroid
            row, col = self.get_cell_from_centroid(cx, cy)
            print(f"{color} is located in cell (row={row}, col={col}).")

        # Draw centroids
        frame = self.draw_centroids(frame, colors)

        # Save image
        cv2.imwrite(filename, frame)

        return frame

    def get_cell_from_centroid(self, cx, cy):
        # ---- Vertical thresholds (columns) ----
        if cx < 260:
            col = 0
        elif cx < 380:
            col = 1
        else:
            col = 2

        # ---- Horizontal thresholds (rows) ----
        if cy < 165:
            row = 2
        elif cy < 295:
            row = 0
        else:
            row = 1

        return (row, col)

    def getColorCell(self, color_name, filename="capture.png"):
        frame = self.snapshot(filename)
        colors = self.detect_colors(frame)

        if color_name not in colors:
            print(f"Color '{color_name}' not detected.")
            return None

        cx, cy = colors[color_name]
        row, col = self.get_cell_from_centroid(cx, cy)

        return (row, col)

