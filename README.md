# go1_resources

ROS2 packages for Unitree Go1 simulation and deployment, built on top of
[unitree_ros2_sim](https://github.com/Atharva-05/unitree_ros2_sim).

## Packages

- **go1sim_bringup** — launchers and configs for the Go1 Gazebo simulation

---

## Installation

### Prerequisites

- ROS2 Humble
- [vcstool](https://github.com/dirk-thomas/vcstool): `pip install vcstool`
- Gazebo 11
- Nav2, slam_toolbox: `sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-slam-toolbox`

### Setup workspace

```bash
mkdir -p ~/go1_ws/src
cd ~/go1_ws

# Import all repositories (unitree_ros2_sim + go1_resources)
vcs import src < src/go1_resources/go1sim.repos
```

> **Note:** `go1sim.repos` is inside `go1_resources/`, which must already be cloned.
> Bootstrap with:
> ```bash
> cd ~/go1_ws/src
> git clone https://github.com/FabPrez/go1_resources.git
> cd ..
> vcs import src < src/go1_resources/go1sim.repos
> ```

### Build

```bash
cd ~/go1_ws
colcon build
source install/setup.bash
```

---

## Launchers

All launchers are in the `go1sim_bringup` package.
The locomotion controller (`junior_ctrl`) must always be started separately
because it requires interactive keyboard input.

### go1sim_bringup

| Command | Description |
|---|---|
| `ros2 launch go1sim_bringup simulation.launch.py` | Gazebo + RViz only (no Nav2) |
| `ros2 launch go1sim_bringup navigation.launch.py` | Nav2 with pre-built map (run after simulation) |
| `ros2 launch go1sim_bringup slam.launch.py` | SLAM + Nav2 (run after simulation) |
| `ros2 launch go1sim_bringup bringup.launch.py` | All-in-one: simulation + Nav2 |
| `ros2 launch go1sim_bringup bringup_slam.launch.py` | All-in-one: simulation + SLAM |

### Locomotion controller (always in a separate terminal)

```bash
ros2 run unitree_guide2 junior_ctrl
# press 2 → stand up
# press 5 → MOVE_BASE mode (accepts /cmd_vel from Nav2)
```

### Typical workflow — navigation with pre-built map

```bash
# Terminal 1
ros2 launch go1sim_bringup bringup.launch.py

# Terminal 2
ros2 run unitree_guide2 junior_ctrl   # press 2, then 5
```

Then use **2D Goal Pose** in RViz to send navigation goals.

### Typical workflow — SLAM (build map while exploring)

```bash
# Terminal 1
ros2 launch go1sim_bringup bringup_slam.launch.py

# Terminal 2
ros2 run unitree_guide2 junior_ctrl   # press 2, then 5
```

Drive the robot around with Nav2 goals or teleop. Save the map when done:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```
