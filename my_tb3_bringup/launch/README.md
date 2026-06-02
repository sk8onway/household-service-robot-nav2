# Launch File Usage Guide

This document explains how to use the custom navigation launch file included in this project.

---

# Prerequisites

Before launching the navigation stack, ensure:

* ROS 2 Humble is installed
* TurtleBot3 packages are installed
* Nav2 is installed
* Gazebo Classic is installed
* The package has been built successfully

```bash
cd ~/roboai_ws

colcon build --packages-select my_tb3_bringup

source install/setup.bash
```

---

# Launching the Navigation Stack

Start the complete navigation system:

```bash
ros2 launch my_tb3_bringup tb3_navigation.launch.py
```

This command automatically launches:

* Gazebo simulation
* TurtleBot3 robot spawn
* Map Server
* AMCL localization
* Nav2 Navigation Stack
* RViz navigation configuration

---

# Verifying Successful Startup

After launch completes:

### Gazebo

The household world should load successfully.

The TurtleBot3 robot should be visible inside the environment.

---

### RViz

RViz should automatically open.

Verify the following are visible:

* Map
* LaserScan
* TF Tree
* Robot Model
* Global Costmap
* Local Costmap

Note: On some machines, the Robot Model may not be visible due to Wayland/X11 rendering conflicts. If this occurs, try switching between display server configurations (Wayland and X11) and relaunching RViz. If the issue persists, it is recommended to verify robot movement using the TF tree and by launching `gzclient` separately to observe the robot directly in Gazebo.

---

### Localization

Confirm AMCL is active:

```bash
ros2 topic list | grep amcl
```

Expected output:

```text
/amcl_pose
/particle_cloud
```

---

### Navigation

Confirm Nav2 action server is available:

```bash
ros2 action list
```

Expected output:

```text
/navigate_to_pose
```

---

# Manual Robot Position Initialization

After startup:

1. Open RViz
2. Select "2D Pose Estimate"
3. Click the robot's location on the map
4. Drag to indicate orientation

This initializes AMCL localization.

---

# Testing Navigation

In RViz:

1. Select "Nav2 Goal"
2. Click a destination on the map
3. Drag to specify orientation

The robot should generate a path and begin navigation.

---

# Running the Full Project

Terminal 1:

```bash
ros2 launch my_tb3_bringup tb3_navigation.launch.py
```

Terminal 2:

```bash
ros2 run my_tb3_bringup room_navigator
```

Terminal 3:

```bash
ros2 run my_tb3_bringup decision_node
```

Terminal 4:

```bash
ros2 run my_tb3_bringup input_node
```

---

# Teleoperation Testing

To manually control the robot:

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

Useful for:

* Localization verification
* Navigation testing
* SLAM map generation
* Demonstration purposes

---

# Useful Debugging Commands

View active nodes:

```bash
ros2 node list
```

View active topics:

```bash
ros2 topic list
```

View active actions:

```bash
ros2 action list
```

Check TF tree:

```bash
ros2 run tf2_tools view_frames
```

Monitor navigation feedback:

```bash
ros2 topic echo /navigate_to_pose/_action/status
```

---

# Shutdown

Stop all nodes safely:

```bash
Ctrl + C
```

in every terminal.

If Gazebo remains active:

```bash
pkill gzserver
pkill gzclient
```

---

# Expected Startup Order

The launch file initializes components in the following sequence:

```text
Gazebo
   ↓
Robot Spawn
   ↓
Map Server
   ↓
AMCL
   ↓
Nav2
   ↓
RViz
```

Users generally do not need to launch any of these components manually.
