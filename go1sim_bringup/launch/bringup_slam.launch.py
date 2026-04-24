"""
Full bringup: simulation + SLAM (builds map while navigating).
Usage:
  ros2 launch go1sim_bringup bringup_slam.launch.py
Then in another terminal:
  ros2 run unitree_guide2 junior_ctrl   # press 2 (stand), then 5 (move_base)
Save the map when done:
  ros2 run nav2_map_server map_saver_cli -f ~/my_map
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    pkg = get_package_share_directory('go1sim_bringup')

    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'simulation.launch.py')))

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'slam.launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'autostart': autostart,
        }.items())

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='True'),
        DeclareLaunchArgument('autostart', default_value='true'),
        simulation,
        slam,
    ])
