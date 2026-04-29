import rclpy
from rclpy.node import Node 
# import threading
from std_msgs.msg import Bool, Empty


class TeeSensorNode(Node):
    def __init__(self):
        super().__init__('tee_sensor_node')
        self.get_logger().info('Tee Sensor Node Started')
        
        # whether the ball is on the tee
        self.ball_present = True
        self.last_ball = None

        # Publisher:
        self.publisher_ = self.create_publisher(Bool, '/tee/ball_present', 10)

        # timer: publish every 0.5 sec
        self.timer = self.create_timer(1.0, self.publish_ball_state)

        self.toggle_subscription = self.create_subscription(Empty, '/sim/toggle_ball', self.toggle_ball_callback, 10)

        # self.input_thread = threading.Thread(target = self.keyboard_loop, daemon = True)
        # self.input_thread.start()

    def publish_ball_state(self):
        # published message: the ball presence status
        msg = Bool()
        msg.data = self.ball_present
        self.publisher_.publish(msg)

        # if the ball presence stautus does not match the last ball status -> state changed -> log
        if self.last_ball != self.ball_present:
            if self.ball_present:
                self.get_logger().info(
                    "Ball State: ON THE TEE"
                )
                self.last_ball = self.ball_present

            else:
                self.get_logger().info(
                    "Ball State: NOT THERE"
                )
                self.last_ball = self.ball_present

    def toggle_ball_callback(self, msg):
        self.ball_present = not self.ball_present

        if self.ball_present:
            self.get_logger().info("Ball detected on tee")
        else:
            self.get_logger().info("Ball hit: tee is now empty")

    # def keyboard_loop(self):
    #     # keyboard input toggles the ball presence
    #     while rclpy.ok():
    #         input()
    #         if self.ball_present == True:
    #             self.ball_present = False
    #             self.get_logger().info('Ball hit: tee is now empty')

    #         else:
    #             self.ball_present = True
    #             self.get_logger().info("Ball detected on the Tee")

    
def main(args = None):
    rclpy.init(args = args)
    node = TeeSensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    