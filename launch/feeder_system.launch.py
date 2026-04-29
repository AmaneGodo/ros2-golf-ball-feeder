from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        Node(
            package = 'ros2_golf_ball_feeder',
            executable = 'tee_sensor_node',
            name = 'tee_sensor_node'
        ), 

        Node(
            package = 'ros2_golf_ball_feeder',
            executable = 'feeder_supervisor_node',
            name = 'feeder_supervisor_node'
        ),

        Node(
            package = 'ros2_golf_ball_feeder',
            executable = 'actuator_node',
            name = 'actuator_node'
        ),
    ])