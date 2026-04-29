import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String

class FeederSupervisorNode(Node):
    def __init__(self):
        super().__init__('feeder_supervisor_node')
        self.get_logger().info('Feeder Supervisor Node Started')

        # subscription: ball presence 
        self.tee = self.create_subscription(Bool, '/tee/ball_present', self.tee_callback, 10)
        # initial tee status : none till receive
        self.latest_tee = None

        # timer
        self.timer = self.create_timer(1.0, self.print_tee)

        # subscription: feed status
        self.feed_status = self.create_subscription(String, '/feeder/status', self.feed_callback, 10)
        self.latest_feed_status = None

        # state:
            # "READY" - when the action is ready
            # "IDLE" - no action needed, stand-by
            # "VERIFYING" - feeding action verification
            # "FAILED" - try feeding again
        self.state = "READY"

        # tries limit when feeding action fails
        self.tries = 3

        # verifying timer start point
        self.verifying_time_start = None

        # time tracker when the ball is no longer present
        self.empty_start_time = None

        # Publisher: command the actuator
        self.command_publisher = self.create_publisher(String, '/feeder/command', 10)



    def tee_callback(self, msg):
        self.latest_tee = msg.data

    def feed_callback(self, msg):
        self.latest_feed_status = msg.data

    def verify_action(self):
        # when called:
            # if the timer has not started -> start the timer and return
            # if it has not been 5 seconds since the timer started -> wait
            # if the ball is not on the tee after 5 sec -> command again

        if (self.verifying_time_start is None):
            self.verifying_time_start = self.get_clock().now() 
            return 

        elapsed_verify = (self.get_clock().now() - self.verifying_time_start).nanoseconds / 1e9

        if (elapsed_verify < 5):
            self.get_logger().info("Checking the ball status")
            return 

        if not self.latest_tee:
            self.get_logger().info("Feeding failed, trying again...")
            self.state = "FAILED"
            self.verifying_time_start = None
            return 

        return 

    def command_feed(self):
        # command actuator to feed

        msg = String()
        msg.data = "FEED_ONE"
        self.command_publisher.publish(msg)
        self.state = "VERIFYING"
        self.get_logger().info("Published command: FEED_ONE")
        return

    def print_tee(self):
        # if no tee data -> wait till it receive the data
        # if ball on the tee and idle -> wait
        # if ball on the tee and "READY" -> first time after ball is fed, prompt the ball is ready to hit
        # if ball is not on the tee:
            # if the timer has not started -> start timer
            # if it has been 3 sec after the time is started -> commmand actuator
            # if msg from actuator is received "DONE" -> verify
            # if feeding failed -> try again
                # if reaches max try attempts -> the ball need to be fed manually

        # pass everything -> reset and return

        if self.latest_tee is None:
            self.get_logger().info("Waiting for the sensor data...")
            return 

        if (self.latest_tee and self.state == ("IDLE")):
            return 

        if self.latest_tee and self.state == ("READY"):
            self.get_logger().info("Ball detected, ready to hit")
            self.empty_start_time = None
            self.tries = 3
            self.state = "IDLE"
            return

        if (not self.latest_tee):
            if self.empty_start_time is None:
                self.empty_start_time = self.get_clock().now()
                return 

            elapsed = (self.get_clock().now() - self.empty_start_time).nanoseconds / 1e9

            if (elapsed >= 3.0 and self.state == "IDLE"):
                self.command_feed()
                return 

            if self.latest_feed_status == "DONE":
                if self.state == "VERIFYING":
                    self.verify_action()
                    return

                if self.state == "FAILED":
                    if self.tries != 0:
                        self.command_feed()
                        self.latest_feed_status = None
                        self.tries -= 1
                        return 

                    else:
                        self.get_logger().info("Feeding failed 3 times. Waiting for a ball to be placed...")

        else:
            self.empty_start_time = None
            self.latest_feed_status = None
            self.verifying_time_start = None
            self.state = "READY"
            return
    
def main(args = None):
    rclpy.init(args = args)
    node = FeederSupervisorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

    