import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg = get_package_share_directory('go1sim_bringup')
    nav2_dir = FindPackageShare('nav2_bringup').find('nav2_bringup')
    nav2_launch_dir = os.path.join(nav2_dir, 'launch')

    map_yaml = os.path.join(pkg, 'map', 'map.yaml')
    nav2_params = os.path.join(pkg, 'params', 'nav2_params.yaml')
    bt_xml = os.path.join(pkg, 'xml', 'go1_bt.xml')

    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='True'),
        DeclareLaunchArgument('autostart', default_value='true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_launch_dir, 'bringup_launch.py')),
            launch_arguments={
                'slam': 'False',
                'map': map_yaml,
                'use_sim_time': use_sim_time,
                'params_file': nav2_params,
                'default_nav_to_pose_bt_xml': bt_xml,
                'default_nav_through_poses_bt_xml': bt_xml,
                'autostart': autostart,
            }.items()),
    ])
