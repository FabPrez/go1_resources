"""
Launches the Go1 simulation in the multi-room world.

Usage:
  ros2 launch go1sim_bringup simulation_multi_room.launch.py

World layout (50 m × 16 m):
  Upper corridor  y = 2 … 8   (full width)
  Spawn room      x = -25 … -10,  y = -8 … 2   (robot starts here)
  Main lower area x = -10 … +25, y = -8 … 2
  Three doorways marked with pink pillars connect the zones.
"""
import os
import xacro

from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_bringup     = get_package_share_directory('go1sim_bringup')
    pkg_gazebo_ros  = get_package_share_directory('gazebo_ros')
    pkg_go1_gazebo  = get_package_share_directory('go1_gazebo')
    pkg_description = get_package_share_directory('go1_description')

    # ── Gazebo model / plugin paths (same logic as go1_gazebo/start_world.launch.py) ──
    install_dir = get_package_prefix('go1_description')
    gazebo_models_path = os.path.join(pkg_go1_gazebo, 'models')

    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] = (
            os.environ['GAZEBO_MODEL_PATH'] + ':' +
            install_dir + '/share' + ':' + gazebo_models_path)
    else:
        os.environ['GAZEBO_MODEL_PATH'] = install_dir + '/share' + ':' + gazebo_models_path

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = (
            os.environ['GAZEBO_PLUGIN_PATH'] + ':' + install_dir + '/lib')
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'

    # ── Robot URDF ────────────────────────────────────────────────────────────
    xacro_file = os.path.join(pkg_description, 'xacro', 'robot.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    # ── World file (inside go1sim_bringup) ────────────────────────────────────
    world_file = os.path.join(pkg_bringup, 'worlds', 'multi_room.world')

    # ── Gazebo ────────────────────────────────────────────────────────────────
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')),
        launch_arguments={
            'world': world_file,
            'verbose': 'false',
        }.items())

    # ── robot_state_publisher ─────────────────────────────────────────────────
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_node',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }])

    # ── Spawn robot in the bottom-left corner of the spawn room ──────────────
    # Corner position keeps only 2 walls visible at start so explore_lite
    # finds real frontiers instead of declaring the room already explored.
    # Spawn room: x=-25…-10, y=-8…2  →  corner with ~1.5 m clearance from walls.
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
            '-entity', 'GO1',
            '-x', '-36.0', '-y', '-4.0', '-z', '0.6',
            '-R', '0.0', '-P', '0.0', '-Y', '0.0',
            '-topic', '/robot_description',
        ])

    # ── ros2_control controllers (unchanged from standard setup) ──────────────
    launch_controllers = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_go1_gazebo, 'launch', 'controllers_go1.launch.py')))

    # ── odom → base_link TF broadcaster ──────────────────────────────────────
    odom_tf_publisher = Node(
        package='go1_navigation',
        executable='nav_tf_publisher',
        name='odom_transform_publisher',
        output='screen')

    # ── RViz with the shared config ────────────────────────────────────────────
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz_node',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', os.path.join(pkg_bringup, 'rviz', 'go1sim.rviz')])

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        launch_controllers,
        odom_tf_publisher,
        rviz,
    ])
