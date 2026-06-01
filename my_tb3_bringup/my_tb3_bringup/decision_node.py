import rclpy

from rclpy.node import Node
from std_msgs.msg import String

from my_tb3_bringup.predict_room import predict_room


class DecisionNode(Node):

    def __init__(self):
        super().__init__("decision_node")

        self.subscription = self.create_subscription(
            String,
            "/task_context",
            self.context_callback,
            10
        )

        self.publisher_ = self.create_publisher(
            String,
            "/target_room",
            10
        )

    def context_callback(self, msg):

        time_of_day, task_type, room_status = (
            msg.data.split(",")
        )

        room = predict_room(
            time_of_day,
            task_type,
            room_status
        )

        room_msg = String()
        room_msg.data = room

        self.publisher_.publish(room_msg)

        self.get_logger().info(
            f"Predicted room: {room}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = DecisionNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()