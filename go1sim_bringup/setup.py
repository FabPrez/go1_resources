from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'go1sim_bringup'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            glob('launch/*.launch.py')),
        ('share/' + package_name + '/params',
            glob('params/*.yaml')),
        ('share/' + package_name + '/map',
            glob('map/*')),
        ('share/' + package_name + '/xml',
            glob('xml/*.xml')),
        ('share/' + package_name + '/rviz',
            glob('rviz/*.rviz')),
        ('share/' + package_name + '/worlds',
            glob('worlds/*.world')),
        ('share/' + package_name + '/map_multi_room',
            glob('map_multi_room/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fabio',
    maintainer_email='gfabiopreziosa@gmail.com',
    description='Bringup package for Go1 simulation',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
