#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from perception_interfaces.msg import TrackedObject
from std_msgs.msg import Float32
from std_msgs.msg import String  # Add this import
from cv_bridge import CvBridge
import cv2
import numpy as np
import time

class OpticalFlowTracker(Node):
    def __init__(self):
        super().__init__('optical_flow_tracker')
        self.bridge = CvBridge()

        self.frame_subscriber = self.create_subscription(
            Image, '/frames', self.image_callback, 10
        )

        self.tracked_objects_subscriber = self.create_subscription(
            TrackedObject, '/tracked_objects', self.tracked_object_callback, 10
        )

        self.speed_publisher = self.create_publisher(Float32, '/estimated_speed', 10)

        self.tracking_status = False
        self.subscription = self.create_subscription(
            String,
            '/tracking_status',
            self.tracking_status_callback,
            10)
        self.subscription

        self.tracked_objects = {}
        self.previous_gray = None
        self.feature_params = dict(maxCorners=50, qualityLevel=0.2, minDistance=5, blockSize=5)
        self.lk_params = dict(winSize=(21, 21), maxLevel=3,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        self.meters_per_pixel = 0.01
        
        self.get_logger().info("Optical Flow Tracker Node Started")

        self.video_ended = False
        self.output_video = None
        self.display_window_name = "Optical Flow with Speed Estimation"

    def tracking_status_callback(self, msg):
        if msg.data == "ready":
            self.tracking_status = True
        else:
            self.tracking_status = False

    def tracked_object_callback(self, msg):
        """Callback to store tracked object bounding boxes from the tracking system."""
        self.tracked_objects[msg.track_id] = {
            'bbox': msg.bbox,
            'history': [],
            'frames_since_seen': 0,
            'last_position': None,
            'last_time': None,
            'class_name': msg.class_name
        }
        self.get_logger().info(f"Tracked object received: ID={msg.track_id}, Class={msg.class_name}, BBox={msg.bbox}")

    def image_callback(self, msg):
        if not self.tracking_status:
            self.get_logger().info('Tracking status not ready')
            return

        if self.video_ended:
            return

        """Processes incoming image frames and computes optical flow."""
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.previous_gray is None:
                self.previous_gray = gray
                height, width, _ = frame.shape
                self.output_video = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
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

                p0 += np.array([[x1, y1]])
                p1, st, err = cv2.calcOpticalFlowPyrLK(self.previous_gray, gray, p0, None, **self.lk_params)

                if p1 is not None and st is not None:
                    good_new = p1[st == 1]
                    good_old = p0[st == 1]

                    obj_data['history'].append(good_new)
                    obj_data['frames_since_seen'] = 0

                    if obj_data['last_position'] is not None and obj_data['last_time'] is not None:
                        displacement = np.linalg.norm(np.mean(good_new - obj_data['last_position'], axis=0))
                        time_diff = current_time - obj_data['last_time']

                        if time_diff > 0:
                            speed_mps = (displacement * self.meters_per_pixel) / time_diff 
                            speed_kph = speed_mps * 3.6 
                            self.get_logger().info(f"Object {obj_id} speed: {speed_kph:.2f} km/h")

                            speed_msg = Float32()
                            speed_msg.data = speed_kph
                            self.speed_publisher.publish(speed_msg)

                            class_name = obj_data.get('class_name', 'Unknown')
                            speed_text = f"ID {obj_id}: {class_name}: {speed_kph:.2f} km/h"
                            cv2.putText(frame, speed_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    obj_data['last_position'] = np.mean(good_new, axis=0)
                    obj_data['last_time'] = current_time

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

            self.output_video.write(frame)

            cv2.imshow(self.display_window_name, frame)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f"Error processing image frame: {e}")

    def destroy_node(self):
        if self.output_video:
            self.output_video.release()
        cv2.destroyWindow(self.display_window_name)
        super().destroy_node()

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
