# ROS2 Object Tracking and Motion Estimation

## Overview

This ROS2 package implements a multi-node system for real-time object tracking and motion estimation. It integrates YOLOv5 for object detection, DeepSORT for object tracking, and Optical Flow for speed estimation. The final fusion node processes and publishes detected objects with unique IDs, class labels, and estimated motion data.

## Features

* **📷 Camera Streamer:** Streams video from a file or webcam.
* **🎯 Object Detection & Tracking:** Uses YOLOv5 for detection and DeepSORT for tracking.
* **📌 Optical Flow Speed Estimation:** Computes object motion vectors.
* **🔀 Data Fusion Node:** Aggregates and publishes detected object data.
* **🛠️ ROS2 Integration:** Modular nodes for easy deployment and scalability.

## Installation

### Prerequisites

Ensure you have the following installed:

* ROS 2 (Humble/Foxy)
* OpenCV
* PyTorch
* TensorRT (optional for acceleration)
* YOLOv5 dependencies (torch, torchvision)
* DeepSORT dependencies (numpy, scipy, sklearn)

### Setup

1.  Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/ros2-object-tracking.git](https://www.google.com/search?q=https://github.com/yourusername/ros2-object-tracking.git)
    cd ros2-object-tracking
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Build the ROS2 workspace:
    ```bash
    colcon build
    source install/setup.bash
    ```

## Usage

### Running the Package

1.  Launch the Camera Streamer:
    ```bash
    ros2 run tracking_package camera_streamer --ros-args -p source:=0
    ```
2.  Run Object Detection and Tracking:
    ```bash
    ros2 run tracking_package object_tracker
    ```
3.  Run Optical Flow Speed Estimation:
    ```bash
    ros2 run tracking_package optical_flow
    ```
4.  Launch the Final Fusion Node:
    ```bash
    ros2 run tracking_package fusion_node
    ```

## Node Descriptions

| Node             | Function                                                     |
| :--------------- | :----------------------------------------------------------- |
| `camera_streamer` | Streams video from a webcam or file.                        |
| `object_tracker`  | Detects and tracks objects using YOLOv5 and DeepSORT.        |
| `optical_flow`    | Computes object motion vectors using Optical Flow.           |
| `fusion_node`     | Aggregates data and publishes fused object information. |

## Topics

| Topic                 | Message Type          | Description                                       |
| :-------------------- | :-------------------- | :------------------------------------------------ |
| `/camera/image_raw`   | `sensor_msgs/Image`   | Raw video stream from the camera.                 |
| `/tracked_objects`    | `tracking_msgs/Objects` | Tracked objects with IDs and labels.              |
| `/motion_vectors`    | `geometry_msgs/Twist` | Motion vectors from optical flow.                 |
| `/final_objects`      | `tracking_msgs/FinalObjects` | Fused object data with tracking information. |

## Future Enhancements

* Support for multi-camera setups.
* Improved object re-identification for occlusions.
* Hardware acceleration with TensorRT for real-time performance.
