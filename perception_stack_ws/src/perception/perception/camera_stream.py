#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import cv2 
import os
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String

class VideoPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, '/frames', 10)
        self.bridge = CvBridge()
        self.video_source = "/home/araby/labs/Robot_Perception_System/perception_stack_ws/src/perception/perception/data/optical_flow.mp4"
        self.cap = cv2.VideoCapture(self.video_source)

        if not self.cap.isOpened():
            self.get_logger().error('Could not open video source')
            return
        
        self.timer = self.create_timer(1.0 / 40.0, self.publish_frame)  # 30 FPS

        self.tracking_status = False
        self.subscription = self.create_subscription(
            String,
            '/tracking_status',
            self.tracking_status_callback,
            10)
        self.subscription

        self.video_ended = False
        self.video_end_publisher = self.create_publisher(String, '/video_end', 10)

    def tracking_status_callback(self, msg):
        if msg.data == "ready":
            self.tracking_status = True
        else:
            self.tracking_status = False

    def publish_frame(self):
        if not self.tracking_status:
            return

        if self.video_ended:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning('Failed to read frame')
            self.video_ended = True
            self.get_logger().info('Video ended')
            end_msg = String()
            end_msg.data = "true"
            self.video_end_publisher.publish(end_msg)
            return
        
        ros_image = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.publisher_.publish(ros_image)
        self.get_logger().info('Published frame')

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = VideoPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
