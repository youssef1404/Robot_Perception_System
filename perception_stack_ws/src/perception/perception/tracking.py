#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import cv2 as cv
import torch
import numpy as np
import random, sys, os
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from perception_interfaces.msg import TrackedObject

from ultralytics import YOLO
sys.path.append("src/perception/perception/")
from perception.tracker_deepsort import Tracker

class ObjectTracker(Node):
    def __init__(self):
        super().__init__("object_tracker")
        self.subscription = self.create_subscription(
            Image, '/frames', self.image_callback, 10
        )
        self.publisher = self.create_publisher(TrackedObject, "/tracked_objects", 10)
        self.bridge = CvBridge()

        self.yolo_model = YOLO('artifacts/yolov5nu.pt')
        self.tracker = Tracker()

        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(10)]
        self.detection_threshold = 0.5

        self.get_logger().info('Object Tracker Initialized')
 
    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        results = self.yolo_model(frame) # return a list of ultralytics.engine.results.Results objects (one per image)

        tracked_objects = []

        for result in results:
            detections = []
            class_names = []
            for r in result.boxes.data.tolist():
                x1, y1, x2, y2, conf, class_id = r  
                class_name = self.yolo_model.names[class_id]
                if conf >= self.detection_threshold:
                    detections.append([int(x1), int(y1), int(x2), int(y2), conf])
                    class_names.append(class_name)
                    self.get_logger().info(f"Detected {class_name} at [{x1}, {y1}, {x2}, {y2}] with confidence {conf:.2f}")

            # Pass detections and class names to the tracker
            self.tracker.update(frame, detections, class_names)

            for track in self.tracker.tracks:
                bbox = track.bbox  
                x1, y1, x2, y2 = bbox
                track_id = track.track_id
                class_name = track.class_name if track.class_name else "Unknown"

                # Create and populate a TrackedObject message
                tracked_obj = TrackedObject()
                tracked_obj.track_id = track_id
                tracked_obj.class_name = class_name
                tracked_obj.bbox = [float(x1), float(y1), float(x2), float(y2)]
                tracked_objects.append(tracked_obj)

                # Draw rectangle
                color = self.colors[track_id % len(self.colors)]
                cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)

                # Draw label with track ID and class name
                label = f"ID {track_id}: {class_name}"
                cv.putText(frame, label, (int(x1), int(y1) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


        # Publish each tracked object individually
        for obj in tracked_objects:
            self.publisher.publish(obj)
            self.get_logger().info(f"Published ID: {obj.track_id} class_name: {obj.class_name} bbox data: {obj.bbox}")
        self.get_logger().info(f"Published {len(tracked_objects)} tracked objects")

        cv.imshow("Tracked Objects", frame)
        cv.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = ObjectTracker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()