import rclpy

from rclpy.node import Node
from std_msgs.msg import String


class InputNode(Node):

    def __init__(self):
        super().__init__("input_node")

        self.publisher_ = self.create_publisher(
            String,
            "/task_context",
            10
        )

        self.publish_context()

    def publish_context(self):

        time_of_day = input(
            "Enter time (morning/afternoon/evening/night): "
        )

        task_type = input(
            "Enter task (delivery/charging/cleaning): "
        )

        room_status = input(
            "Enter room status (low/medium/high): "
        )

        msg = String()
        msg.data = (
            f"{time_of_day},{task_type},{room_status}"
        )

        self.publisher_.publish(msg)

        self.get_logger().info(
            f"Published: {msg.data}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = InputNode()

    rclpy.spin_once(node, timeout_sec=1.0)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()