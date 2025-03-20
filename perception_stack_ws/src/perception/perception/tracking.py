#!/usr/bin/env python3

import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "artifacts/mars-small128.pb")

import sys
import random
import logging
from typing import List, Tuple, Dict, Any

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from perception_interfaces.msg import TrackedObject

from ultralytics import YOLO

# Add the perception module to the system path
sys.path.append("src/perception/perception/")
from perception.tracker_deepsort import Tracker


class ObjectTracker(Node):
    """
    ROS2 Node for detecting and tracking objects in image frames.
    Uses YOLO for detection and DeepSORT for tracking.
    """

    def __init__(self):
        super().__init__("object_tracker")
        
        self._setup_ros_communication()
        self._setup_cv_components()
        self._setup_visualization()

        self.get_logger().info('Object Tracker Initialized')
    
    def _setup_ros_communication(self) -> None:
        """Set up ROS2 publishers and subscribers."""
        self.subscription = self.create_subscription(
            Image, '/frames', self.image_callback, 10
        )
        self.publisher = self.create_publisher(
            TrackedObject, "/tracked_objects", 10
        )
        self.bridge = CvBridge()
    
    def _setup_cv_components(self) -> None:
        """Set up computer vision components including models and trackers."""
        try:
            self.yolo_model = YOLO('artifacts/yolov5nu.pt')
            self.tracker = Tracker()
            self.detection_threshold = 0.5
        except Exception as e:
            self.get_logger().error(f"Failed to initialize CV components: {str(e)}")
            raise
    
    def _setup_visualization(self) -> None:
        """Set up visualization components."""
        self.colors = [
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for _ in range(10)
        ]
        self.show_visualization = True
    
    def image_callback(self, msg: Image) -> None:
        """
        Process incoming image frames, detect and track objects.
        
        Args:
            msg: ROS Image message containing the frame to process
        """
        try:
            # Convert ROS Image message to OpenCV image
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # Run object detection
            detections, class_names = self._detect_objects(frame)
            
            # Update tracker with new detections
            self.tracker.update(frame, detections, class_names)
            
            # Process and publish tracked objects
            tracked_objects = self._process_tracked_objects(frame)
            
            # Publish tracked objects
            self._publish_tracked_objects(tracked_objects)
            
            # Display visualization if enabled
            if self.show_visualization:
                cv2.imshow("Tracked Objects", frame)
                cv2.waitKey(1)
                
        except Exception as e:
            self.get_logger().error(f"Error in image callback: {str(e)}")
    
    def _detect_objects(self, frame: np.ndarray) -> Tuple[List[List[float]], List[str]]:
        """
        Detect objects in the frame using YOLO.
        
        Args:
            frame: Input image frame
            
        Returns:
            Tuple containing lists of detections and class names
        """
        detections = []
        class_names = []
        
        results = self.yolo_model(frame)
        
        for result in results:
            for r in result.boxes.data.tolist():
                x1, y1, x2, y2, conf, class_id = r
                if conf >= self.detection_threshold:
                    class_name = self.yolo_model.names[int(class_id)]
                    detections.append([int(x1), int(y1), int(x2), int(y2), conf])
                    class_names.append(class_name)
                    self.get_logger().debug(
                        f"Detected {class_name} at [{x1}, {y1}, {x2}, {y2}] with confidence {conf:.2f}"
                    )
        
        return detections, class_names
    
    def _process_tracked_objects(self, frame: np.ndarray) -> List[TrackedObject]:
        """
        Process tracked objects and prepare them for publishing.
        
        Args:
            frame: Current image frame (will be modified with visualization)
            
        Returns:
            List of TrackedObject messages
        """
        tracked_objects = []
        
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
            
            # Draw visualization elements
            if self.show_visualization:
                self._draw_track_visualization(frame, track_id, class_name, bbox)
        
        return tracked_objects
    
    def _draw_track_visualization(self, frame: np.ndarray, track_id: int, 
                                 class_name: str, bbox: List[float]) -> None:
        """
        Draw visualization elements for a tracked object.
        
        Args:
            frame: Image frame to draw on
            track_id: ID of the track
            class_name: Class name of the detected object
            bbox: Bounding box coordinates [x1, y1, x2, y2]
        """
        x1, y1, x2, y2 = bbox
        color = self.colors[track_id % len(self.colors)]
        
        # Draw rectangle
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)
        
        # Draw label with track ID and class name
        label = f"ID {track_id}: {class_name}"
        cv2.putText(frame, label, (int(x1), int(y1) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    def _publish_tracked_objects(self, tracked_objects: List[TrackedObject]) -> None:
        """
        Publish tracked objects to ROS topic.
        
        Args:
            tracked_objects: List of TrackedObject messages to publish
        """
        for obj in tracked_objects:
            self.publisher.publish(obj)
            self.get_logger().debug(
                f"Published ID: {obj.track_id} class_name: {obj.class_name} bbox data: {obj.bbox}"
            )
        
        self.get_logger().info(f"Published {len(tracked_objects)} tracked objects")


def main(args=None):
    """Main function to initialize and run the node."""
    try:
        # Initialize ROS2
        rclpy.init(args=args)
        
        # Create and spin the node
        node = ObjectTracker()
        rclpy.spin(node)
        
    except Exception as e:
        logging.error(f"Error running ObjectTracker node: {str(e)}")
        
    finally:
        # Clean up
        if 'node' in locals():
            node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
