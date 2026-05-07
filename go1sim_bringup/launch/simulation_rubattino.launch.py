"""
Launches the Go1 simulation in the Rubattino 3D world.
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

    install_dir = get_package_prefix('go1_description')
    gazebo_models_path = os.path.join(pkg_go1_gazebo, 'models')
    
    bringup_models_path = os.path.join(pkg_bringup, 'models')

    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] = (
            os.environ['GAZEBO_MODEL_PATH'] + ':' +
            install_dir + '/share' + ':' + gazebo_models_path + ':' + bringup_models_path)
    else:
        os.environ['GAZEBO_MODEL_PATH'] = install_dir + '/share' + ':' + gazebo_models_path + ':' + bringup_models_path

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = (
            os.environ['GAZEBO_PLUGIN_PATH'] + ':' + install_dir + '/lib')
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'

    xacro_file = os.path.join(pkg_description, 'xacro', 'robot.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    world_file = os.path.join(pkg_bringup, 'worlds', 'rubattino.world')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')),
        launch_arguments={
            'world': world_file,
            'verbose': 'false',
        }.items())

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_node',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }])

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
            '-entity', 'GO1',
            '-x', '100.0', '-y', '5.0', '-z', '0.6',
            '-R', '0.0', '-P', '0.0', '-Y', '0.0',
            '-topic', '/robot_description',
        ])

    launch_controllers = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_go1_gazebo, 'launch', 'controllers_go1.launch.py')))

    odom_tf_publisher = Node(
        package='go1_navigation',
        executable='nav_tf_publisher',
        name='odom_transform_publisher',
        output='screen')

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
