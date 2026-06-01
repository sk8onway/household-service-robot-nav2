import math
import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped, Quaternion
from nav2_msgs.action import NavigateToPose
from std_msgs import msg
from std_msgs.msg import String

ROOMS = {
    "bedroom": {
        "x": -6.2431,
        "y": -0.1596,
        "yaw": -1.4716,
    },
    "kitchen": {
        "x": 4.9807,
        "y": 2.7082,
        "yaw": 2.2543,
    },
    "livingroom": {
        "x": -2.4049,
        "y": 4.0361,
        "yaw": -0.0241,
    },
}



class RoomNavigator(Node):
    """Simple ROS 2 node that sends a single Nav2 navigate_to_pose goal."""

    def __init__(self):
        super().__init__("room_navigator")

        self.subscription = self.create_subscription(
        String,
        "/target_room",
        self.room_callback,
        10
        )

        # Create an action client for the Nav2 NavigateToPose action.
        self._action_client = ActionClient(self, NavigateToPose, "/navigate_to_pose")

        # Wait for the Nav2 action server to be available before sending a goal.
        self.get_logger().info("Waiting for Nav2...")
        self._action_client.wait_for_server()

        # Send the hardcoded room goal once the server is ready.
        # self.send_room_goal(ROOM)

    def room_callback(self, msg):

        room = msg.data

        self.get_logger().info(
            f"Received room: {room}"
        )

        self.send_room_goal(room)

    @staticmethod
    def quaternion_from_yaw(yaw: float) -> Quaternion:
        """Convert a yaw angle (rad) into a quaternion for a planar pose."""
        half_yaw = yaw * 0.5
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(half_yaw)
        q.w = math.cos(half_yaw)
        return q

    def create_pose_stamped(self, room_name: str) -> PoseStamped:
        """Build a PoseStamped message for the requested room."""
        room = ROOMS[room_name]
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = room["x"]
        pose.pose.position.y = room["y"]
        pose.pose.position.z = 0.0
        pose.pose.orientation = self.quaternion_from_yaw(room["yaw"])
        return pose

    def send_room_goal(self, room_name: str) -> None:
        """Send a NavigateToPose goal to the Nav2 action server."""
        self.get_logger().info(f"Sending goal for room: {room_name}")

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = self.create_pose_stamped(room_name)

        self._goal_future = self._action_client.send_goal_async(goal_msg)
        self._goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle the Nav2 goal response and monitor acceptance/rejection."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Goal rejected by Nav2")
            rclpy.shutdown()
            return

        self.get_logger().info("Goal accepted")
        self._result_future = goal_handle.get_result_async()
        self._result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """Handle the result returned by Nav2 when navigation completes."""
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Navigation succeeded")
        else:
            self.get_logger().error(f"Navigation failed with status: {status}")
            if result is not None and hasattr(result, "error_code"):
                self.get_logger().error(f"Nav2 error code: {result.error_code}")

        rclpy.shutdown()


def main(args=None):
    """Initialize the ROS 2 node and spin until the action result is received."""
    rclpy.init(args=args)
    node = RoomNavigator()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt received, shutting down")
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
