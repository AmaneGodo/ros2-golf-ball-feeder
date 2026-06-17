import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String
import serial


class SerialBridgeNode(Node):
    def __init__(self):
        super().__init__("serial_bridge_node")

        self.publisher = self.create_publisher(Bool, "/tee/ball_present", 10)

        self.ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)

        self.timer = self.create_timer(0.05, self.read_serial)

        self.get_logger().info("Serial bridge connected to ESP32 on /dev/ttyUSB0")

        self.feed_command = self.create_subscription(String, "/feeder/command", self.feed_command_callback, 10)

    def read_serial(self):
        line = self.ser.readline().decode(errors="ignore").strip()

        if line == "BALL_PRESENT":
            msg = Bool()
            msg.data = True
            self.publisher.publish(msg)
            self.get_logger().info("Published: ball_present = True")

        elif line == "BALL_MISSING":
            msg = Bool()
            msg.data = False
            self.publisher.publish(msg)
            self.get_logger().info("Published: ball_present = False")

    def feed_command_callback(self, msg):
        command = msg.data.strip()

        if command == "FEED_ONE":
            self.get_logger().info("Sending FEED_ONE to ESP32")
            self.ser.write(b"FEED_ONE\n")



def main(args=None):
    rclpy.init(args=args)
    node = SerialBridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()