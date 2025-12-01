# SO-101 Robot Arm Integration Guide

## What Changed from Simulation to Real Robot

### Current Files

- `detect_colors.py` - Original PyBullet simulation
- `complete_sorting_system.py` - Complete simulation
- `shape_recognition.py` - Shape detection (not using)
- All other images and test files

### New Files for Real Robot

1. **`detect_colors_real_camera.py`** - Test color detection with real camera
2. **`teach_waypoints.py`** - Record robot positions
3. **`so101_sorting_controller.py`** - Complete sorting system

---

## Step-by-Step Setup

### Phase 1: Test Camera (5 minutes)

1. **Connect your camera** to the computer
2. **Run the camera test:**

   ```bash
   python detect_colors_real_camera.py
   ```

3. **Place colored objects** in view of camera
4. **Check the output images:**
   - `original_image_real.png` - Raw camera image
   - `color_detection_result_real.png` - Detected colors highlighted

**If colors aren't detected:**

- Adjust lighting (avoid shadows, backlighting)
- Try different `CAMERA_ID` (0, 1, or 2) in the script
- Adjust HSV ranges if needed

---

### Phase 2: Record Robot Positions (30-60 minutes)

1. **Connect SO-101** to computer (check COM port in Device Manager)
2. **Update PORT** in `teach_waypoints.py` if needed (default is COM4)
3. **Run the teaching script:**

   ```bash
   python teach_waypoints.py
   ```

4. **Follow the prompts** to manually move robot and record each position:
   - Home position (safe starting point)
   - 3 pickup positions (approach, grasp, lift for each)
   - 3 drop positions (one for each color)

**Tips:**

- Take your time positioning accurately
- Test each position before recording
- Make sure gripper can reach without collisions
- Keep positions consistent with where you'll place shapes

**Output:** Creates `sorting_waypoints.json` with all positions

---

### Phase 3: Run Sorting (Demo Time!)

1. **Place colored shapes** at the 3 pickup positions you recorded
2. **Update configuration** in `so101_sorting_controller.py` if needed:
   - PORT (COM port)
   - CAMERA_ID (0, 1, or 2)
   - GRIPPER_OPEN / GRIPPER_CLOSED (test to find right values)

3. **Run the sorting system:**

   ```bash
   python so101_sorting_controller.py
   ```

4. **Watch it work!**
   - Camera detects colors
   - Robot picks up each shape
   - Sorts into correct slots

---

## Configuration Settings

### In `teach_waypoints.py`

```python
PORT = "COM4"  # Change to your SO-101 COM port
ROBOT_ID = "my_awesome_follower_arm"
```

### In `so101_sorting_controller.py`

```python
PORT = "COM4"
CAMERA_ID = 0  # Try 0, 1, or 2
GRIPPER_OPEN = 0.0    # Adjust based on your gripper
GRIPPER_CLOSED = 50.0  # Adjust based on your gripper
```

### Color Detection (if needed)

In both `detect_colors_real_camera.py` and `so101_sorting_controller.py`:

```python
color_ranges = {
    'red': {
        'lower': np.array([0, 100, 100]),    # Adjust these
        'upper': np.array([10, 255, 255]),   # if colors not detected
    },
    # ... same for green and blue
}
```

---

## Troubleshooting

### Camera Issues

**Problem:** "Could not read from camera"

- **Solution:** Try different CAMERA_ID (0, 1, or 2)
- Check camera is connected
- Close other apps using camera

**Problem:** Colors not detected

- **Solution:** Improve lighting (bright, even lighting)
- Adjust HSV ranges
- Increase minimum area threshold

### Robot Issues

**Problem:** "Could not connect to robot"

- **Solution:** Check COM port in Device Manager
- Update PORT in script
- Check USB connection

**Problem:** Robot moves too fast/jerky

- **Solution:** Increase `wait_time` in `move_to_waypoint()`
- Add more intermediate waypoints

**Problem:** Gripper doesn't close/open

- **Solution:** Adjust GRIPPER_OPEN and GRIPPER_CLOSED values
- Test manually first

### Waypoint Issues

**Problem:** "Waypoint not found"

- **Solution:** Run `teach_waypoints.py` again
- Check `sorting_waypoints.json` exists
- Make sure all waypoints were recorded
