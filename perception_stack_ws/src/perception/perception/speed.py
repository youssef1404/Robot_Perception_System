#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from perception_interfaces.msg import TrackedObject
from cv_bridge import CvBridge
import cv2
import numpy as np
import time

class OpticalFlowTracker(Node):
    def __init__(self):
        super().__init__('optical_flow_tracker')
        self.bridge = CvBridge()

        # Image Subscriber
        self.frame_subscriber = self.create_subscription(
            Image, '/frames', self.image_callback, 10
        )

        # Tracked Object Subscriber
        self.tracked_objects_subscriber = self.create_subscription(
            TrackedObject, '/tracked_objects', self.tracked_object_callback, 10
        )

        self.tracked_objects = {}  # Store objects with a history of positions
        self.previous_gray = None
        self.feature_params = dict(maxCorners=50, qualityLevel=0.2, minDistance=5, blockSize=5)
        self.lk_params = dict(winSize=(21, 21), maxLevel=3,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        self.meters_per_pixel = 0.01  # Example calibration factor (adjust based on your setup)
        
        self.get_logger().info("Optical Flow Tracker Node Started")

    def tracked_object_callback(self, msg):
        """Callback to store tracked object bounding boxes from the tracking system."""
        self.tracked_objects[msg.track_id] = {
            'bbox': msg.bbox,
            'history': [],
            'frames_since_seen': 0,
            'last_position': None,
            'last_time': None
        }
        self.get_logger().info(f"Tracked object received: ID={msg.track_id}, Class={msg.class_name}, BBox={msg.bbox}")

    def image_callback(self, msg):
        """Processes incoming image frames and computes optical flow."""
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.previous_gray is None:
                self.previous_gray = gray
                return

            if not self.tracked_objects:
                self.get_logger().warn("No tracked objects received yet.")
                return

            new_tracked_objects = {}
            current_time = time.time()

            for obj_id, obj_data in self.tracked_objects.items():
                try:
                    x1, y1, x2, y2 = [int(coord) for coord in obj_data['bbox']]
                except ValueError:
                    self.get_logger().error(f"Invalid bbox format: {obj_data['bbox']}")
                    continue

                if x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
                    self.get_logger().warn(f"Skipping out-of-bounds bbox: {x1, y1, x2, y2}")
                    continue

                roi = self.previous_gray[y1:y2, x1:x2]

                if roi.size == 0:
                    self.get_logger().warn("Skipping empty ROI.")
                    continue

                p0 = cv2.goodFeaturesToTrack(roi, mask=None, **self.feature_params)

                if p0 is None:
                    self.get_logger().warn("No good features found in ROI.")
                    continue

                p0 += np.array([[x1, y1]])  # Adjust coordinates to full frame
                p1, st, err = cv2.calcOpticalFlowPyrLK(self.previous_gray, gray, p0, None, **self.lk_params)

                if p1 is not None and st is not None:
                    good_new = p1[st == 1]
                    good_old = p0[st == 1]

                    obj_data['history'].append(good_new)
                    obj_data['frames_since_seen'] = 0

                    # Speed estimation
                    if obj_data['last_position'] is not None and obj_data['last_time'] is not None:
                        displacement = np.linalg.norm(np.mean(good_new - obj_data['last_position'], axis=0))
                        time_diff = current_time - obj_data['last_time']

                        if time_diff > 0:
                            speed_mps = (displacement * self.meters_per_pixel) / time_diff  # Speed in m/s
                            speed_kph = speed_mps * 3.6  # Convert to km/h
                            self.get_logger().info(f"Object {obj_id} speed: {speed_kph:.2f} km/h")

                            # Display speed on image
                            speed_text = f"{speed_kph:.2f} km/h"
                            cv2.putText(frame, speed_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Update last position and time
                    obj_data['last_position'] = np.mean(good_new, axis=0)
                    obj_data['last_time'] = current_time

                    # Draw bounding box and optical flow vectors
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    for new, old in zip(good_new, good_old):
                        a, b = new.ravel()
                        c, d = old.ravel()
                        cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                        cv2.circle(frame, (int(a), int(b)), 5, (0, 0, 255), -1)

                    new_tracked_objects[obj_id] = obj_data
                else:
                    obj_data['frames_since_seen'] += 1
                    if obj_data['frames_since_seen'] < 5:
                        new_tracked_objects[obj_id] = obj_data
                    else:
                        self.get_logger().warn(f"Lost tracking for object ID {obj_id}")

            self.tracked_objects = new_tracked_objects
            self.previous_gray = gray.copy()

            cv2.imshow("Optical Flow with Speed Estimation", frame)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f"Error processing image frame: {e}")


def main():
    rclpy.init()
    node = OpticalFlowTracker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Optical Flow Tracker Node...")
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
