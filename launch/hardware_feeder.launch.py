from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="ros2_golf_ball_feeder",
            executable="serial_bridge_node",
            name="serial_bridge_node",
            output="screen",
        ),
        Node(
            package="ros2_golf_ball_feeder",
            executable="feeder_supervisor_node",
            name="feeder_supervisor_node",
            output="screen",
        ),
    ])