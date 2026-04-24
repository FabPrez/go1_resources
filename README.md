# go1_resources

ROS2 packages for Unitree Go1 simulation and deployment.

## Packages

### go1sim_bringup

Bringup package for the Go1 Gazebo simulation. Provides launchers and configs
that work on top of [unitree_ros2_sim](https://github.com/unitreerobotics/unitree_ros2_sim)
without modifying it.

**Dependencies:** `go1_gazebo`, `go1_description`, `go1_navigation`, `nav2_bringup`, `slam_toolbox`

**Launchers:**

| Launch file | Description |
|---|---|
| `simulation.launch.py` | Gazebo + RViz only |
| `navigation.launch.py` | Nav2 with pre-built map |
| `slam.launch.py` | SLAM + Nav2 |
| `bringup.launch.py` | Simulation + Nav2 (all-in-one) |
| `bringup_slam.launch.py` | Simulation + SLAM (all-in-one) |

**Usage:**
```bash
# Clone inside your ROS2 workspace src/
cd ~/your_ws/src
git clone https://github.com/FabPrez/go1_resources.git

# Build
cd ~/your_ws
colcon build --packages-select go1sim_bringup
source install/setup.bash

# Run
ros2 launch go1sim_bringup bringup.launch.py
# In another terminal:
ros2 run unitree_guide2 junior_ctrl   # press 2 (stand), 5 (move_base)
```
