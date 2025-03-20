#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import cv2 
import os
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class VideoPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, '/frames', 10)
        self.bridge = CvBridge()
        
        self.video_source = "/home/hunter/Speed_ws/src/optical_flow/challenge.mp4"
        # self.video_source = os.path.abspath(os.path.join("data", "people.mp4"))        
        self.cap = cv2.VideoCapture(self.video_source)

        if not self.cap.isOpened():
            self.get_logger().error('Could not open video source')
            return
        
        self.timer = self.create_timer(1.0 / 40.0, self.publish_frame)  # 30 FPS

    def publish_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning('Failed to read frame')
            return
        
        # Convert frame to ROS Image message
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
