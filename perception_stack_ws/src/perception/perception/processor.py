#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from perception_interfaces.msg import TrackedObject
from std_msgs.msg import Float32, String
import time

class ProcessorNode(Node):
    def __init__(self):
        super().__init__('processor')
        self.create_subscription(TrackedObject, '/tracked_objects', self.tracking_callback, 10)
        self.create_subscription(Float32, '/estimated_speed', self.speed_callback, 10)
        self.create_subscription(String, '/tracking_status', self.tracking_status_callback, 10)
        self.create_subscription(String, '/video_end', self.video_end_callback, 10)
        self.final_publisher = self.create_publisher(String, '/final_object_list', 10)
        self.last_tracking_msg = None
        self.last_speed_msg = None
        self.last_message_time = time.time()
        self.tracking_status = False
        self.video_ended = False
        self.object_records = {}
        self.timer = self.create_timer(0.1, self.process_synchronized_messages)
        self.get_logger().info('Processor Node Initialized (manual sync without segmentation)')

    def tracking_callback(self, msg: TrackedObject):
        self.last_tracking_msg = msg

    def speed_callback(self, msg: Float32):
        self.last_speed_msg = msg

    def tracking_status_callback(self, msg: String):
        if msg.data.lower() == "ready":
            self.tracking_status = True
            self.get_logger().info('Tracking status set to ready')
        else:
            self.tracking_status = False
            self.get_logger().info('Tracking status set to not ready')

    def video_end_callback(self, msg: String):
        self.get_logger().info(f"Received video end message: {msg.data}")
        if msg.data.lower() == "true":
            self.video_ended = True
            self.log_final_objects()
            self.get_logger().info("Video ended")
            self.destroy_node()

    def process_synchronized_messages(self):
        if self.last_tracking_msg is None or self.last_speed_msg is None:
            return

        if not self.tracking_status or self.video_ended:
            return

        self.get_logger().info("Processing synchronized messages (manual sync)")

        tracking_msg = self.last_tracking_msg
        speed_msg = self.last_speed_msg
        self.last_tracking_msg = None
        self.last_speed_msg = None

        track_id = tracking_msg.track_id
        class_name = tracking_msg.class_name
        bbox = tracking_msg.bbox
        speed_kph = speed_msg.data

        if track_id not in self.object_records:
            self.object_records[track_id] = {
                'class': class_name,
                'bbox': bbox,
                'speeds': []
            }
        self.object_records[track_id]['speeds'].append(speed_kph)
        speeds = self.object_records[track_id]['speeds']
        avg_speed = sum(speeds) / len(speeds) if speeds else 0

        self.get_logger().info(
            f"Live Object Data - ID: {track_id}, Class: {class_name}, "
            f"BBox: {bbox}, Current Speed: {speed_kph:.2f} km/h, "
            f"Avg Speed: {avg_speed:.2f} km/h"
        )

        object_info = {
            'id': track_id,
            'class': class_name,
            'bbox': bbox,
            'speed_kph': speed_kph
        }
        final_msg = String()
        final_msg.data = str(object_info)
        self.final_publisher.publish(final_msg)

        self.last_message_time = time.time()

    def log_final_objects(self):
        self.get_logger().info("Video ended. Logging all tracked objects with their average speed:")
        for track_id, data in self.object_records.items():
            avg_speed = sum(data['speeds']) / len(data['speeds']) if data['speeds'] else 0
            self.get_logger().info(
                f"ID: {track_id}, Class: {data['class']}, BBox: {data['bbox']}, "
                f"Avg Speed: {avg_speed:.2f} km/h"
            )

def main():
    rclpy.init()
    node = ProcessorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
