import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (IncludeLaunchDescription, GroupAction)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions.node import Node

def generate_launch_description():
    # Path
    nb2_launch_dir = os.path.join(get_package_share_directory('neuronbot2_bringup'), 'launch')
    nb2nav_launch_dir = os.path.join(get_package_share_directory('neuronbot2_slam'), 'launch')

    # Parameters
    open_rviz = LaunchConfiguration('open_rviz', default='True')

    neuron_app_bringup = GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(nb2_launch_dir, 'bringup_launch.py'))),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(nb2nav_launch_dir, 'gmapping_launch.py')),
            launch_arguments={'open_rviz': open_rviz}.items()),
    ])

    # Run mouse teleop
    mouse_teleop = Node(
        package='mouse_teleop',
        executable='mouse_teleop',
        remappings=[('mouse_vel', 'cmd_vel')],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(neuron_app_bringup)
    ld.add_action(mouse_teleop)
    return ld
