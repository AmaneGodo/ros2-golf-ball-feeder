import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ActuatorNode(Node):
    def __init__(self):
        super().__init__('actuator_node')
        self.get_logger().info('Actuator Node Started')

        self.command = self.create_subscription(String, '/feeder/command', self.command_callback, 10)
        self.latest_command = None

        self.timer = self.create_timer(1.0, self.command_process)
        self.action_start_time = None

        self.action_complete = 0 # 0 for not complete, 1 for in action

        self.status_publisher = self.create_publisher(String, '/feeder/status', 10)

    def command_callback(self, msg):
        self.latest_command = msg.data

    def command_process(self):
        if self.latest_command is None:
            return

        if self.latest_command == "FEED_ONE":
            if self.action_complete == 0:
                self.action_start_time = self.get_clock().now()
                self.action_complete = 1
                self.get_logger().info("Servo rotating 90 degrees")
                return

            elapsed = (self.get_clock().now() - self.action_start_time).nanoseconds / 1e9

            if (self.action_complete == 1 and (elapsed > 3)):
                status = String()
                status.data = "DONE"
                self.status_publisher.publish(status)
                self.get_logger().info('The ball feeding complete')
                self.latest_command = None
                self.action_complete = 0
                return 

def main(args = None):
    rclpy.init(args = args)
    node = ActuatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()