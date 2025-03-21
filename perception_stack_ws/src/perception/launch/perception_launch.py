from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='perception',
            executable='camera_stream',
            name='camera_stream'
        ),
        Node(
            package='perception',
            executable='tracking',
            name='tracking'
        ),
        Node(
            package='perception',
            executable='speed',
            name='speed'
        ),
        Node(
            package='perception',
            executable='processor',
            name='processor'
        ),
    ])
