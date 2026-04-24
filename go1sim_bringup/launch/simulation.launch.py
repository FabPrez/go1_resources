"""
Launches the Go1 simulation: Gazebo world, robot spawn, controllers, RViz.
Replaces go1_gazebo/spawn_go1.launch.py using our own RViz config.
"""
import os
import xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_bringup = get_package_share_directory('go1sim_bringup')
    pkg_gazebo = get_package_share_directory('go1_gazebo')
    pkg_description = get_package_share_directory('go1_description')

    world_file_name = LaunchConfiguration('world_file_name')
    urdf_file = LaunchConfiguration('urdf_file')

    # --- Robot description ---
    xacro_file = os.path.join(pkg_description, 'xacro', 'robot.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    # --- Gazebo world ---
    start_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo, 'launch', 'start_world.launch.py')),
        launch_arguments={'world_file_name': world_file_name}.items())

    # --- Spawn robot ---
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
            '-entity', 'GO1',
            '-x', '0', '-y', '0', '-z', '0.6',
            '-R', '0', '-P', '0', '-Y', '0',
            '-topic', '/robot_description'])

    # --- robot_state_publisher ---
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_node',
        output='screen',
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': True}])

    # --- ros2_control controllers ---
    launch_controllers = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo, 'launch', 'controllers_go1.launch.py')))

    # --- odom → base_link TF broadcaster ---
    odom_tf_publisher = Node(
        package='go1_navigation',
        executable='nav_tf_publisher',
        name='odom_transform_publisher',
        output='screen')

    # --- RViz with our custom config ---
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz_node',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', os.path.join(pkg_bringup, 'rviz', 'go1sim.rviz')])

    return LaunchDescription([
        DeclareLaunchArgument('world_file_name', default_value='test_latest.world'),
        DeclareLaunchArgument('urdf_file', default_value='robot.xacro'),
        start_world,
        robot_state_publisher,
        spawn_robot,
        launch_controllers,
        odom_tf_publisher,
        rviz,
    ])
