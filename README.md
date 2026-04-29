# go1_resources

ROS2 packages for Unitree Go1 simulation and deployment, built on top of
[unitree_ros2_sim](https://github.com/Atharva-05/unitree_ros2_sim) and
[m-explore-ros2](https://github.com/robo-friends/m-explore-ros2).

## Packages

- **go1sim_bringup** — launchers and configs for the Go1 Gazebo simulation

---

## Installation

### Prerequisites

- ROS2 Humble
- [vcstool](https://github.com/dirk-thomas/vcstool): `pip install vcstool`
- Gazebo 11
- Nav2, slam_toolbox: `sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-slam-toolbox`
- lcm (Needs to be built from source)

### Setup workspace

```bash
mkdir -p /go1_ws/src
cd /go1_ws/src

git clone https://github.com/FabPrez/go1_resources.git
sudo apt update
sudo apt dist-upgrade
rosdep update
vcs import src < go1_resources/go1sim.repos
cd ..
rosdep install -r --from-paths . --ignore-src --rosdistro $ROS_DISTRO -y


```


### Build

```bash
cd /go1_ws
colcon build --symlink-install   --parallel-workers 2   --cmake-args -DCMAKE_BUILD_PARALLEL_LEVEL=2
source install/setup.bash
```

---

## Launchers

Each concern is launched separately in its own terminal. The three groups are:

| Group | Command | Description |
|---|---|---|
| **Simulation** | `ros2 launch go1sim_bringup simulation.launch.py` | Gazebo world + robot spawn + RViz |
| **Controller** | `ros2 run unitree_guide2 junior_ctrl` | Locomotion controller (requires keyboard input) |
| **Nav2 — map** | `ros2 launch go1sim_bringup navigation.launch.py` | Nav2 with pre-built map (AMCL localization) |
| **Nav2 — SLAM** | `ros2 launch go1sim_bringup slam.launch.py` | slam_toolbox + Nav2 (builds map on the fly) |
| **Autonomous exploration** | `ros2 launch explore_lite explore.launch.py` | Frontier-based autonomous SLAM (requires SLAM running) |

> **Note:** `junior_ctrl` always runs in its own terminal because it requires interactive keyboard input (`2` → stand up, `5` → MOVE_BASE mode).

---

## Typical workflow — navigation with pre-built map

```bash
# Terminal 1 — simulation
ros2 launch go1sim_bringup simulation.launch.py

# Terminal 2 — locomotion controller
ros2 run unitree_guide2 junior_ctrl
# press 2 → stand up
# press 5 → MOVE_BASE mode (accepts /cmd_vel from Nav2)

# Terminal 3 — Nav2 stack (after the robot is standing)
ros2 launch go1sim_bringup navigation.launch.py
```

Then use **2D Goal Pose** in RViz to send navigation goals.

---

## Typical workflow — SLAM (build map while exploring)

```bash
# Terminal 1 — simulation
ros2 launch go1sim_bringup simulation.launch.py

# Terminal 2 — locomotion controller
ros2 run unitree_guide2 junior_ctrl
# press 2 → stand up
# press 5 → MOVE_BASE mode (accepts /cmd_vel from Nav2)

# Terminal 3 — SLAM + Nav2 (after the robot is standing)
ros2 launch go1sim_bringup slam.launch.py
```

Drive the robot around with Nav2 goals or teleop. Save the map when done:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

---

## Typical workflow — autonomous SLAM (robot explores on its own)

The robot autonomously identifies unexplored frontiers and navigates to them until the entire environment is mapped.

```bash
# Terminal 1 — simulation
ros2 launch go1sim_bringup simulation.launch.py

# Terminal 2 — locomotion controller
ros2 run unitree_guide2 junior_ctrl
# press 2 → stand up
# press 5 → MOVE_BASE mode (accepts /cmd_vel from Nav2)

# Terminal 3 — SLAM + Nav2 (after the robot is standing)
ros2 launch go1sim_bringup slam.launch.py

# Terminal 4 — autonomous exploration (after SLAM is active)
ros2 launch explore_lite explore.launch.py
```

The robot will autonomously explore the environment building the map. When exploration is complete (no more frontiers), save the map:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```
