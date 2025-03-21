import rclpy
from rclpy.node import Node
import cv2
from ultralytics import YOLO
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class segmentation(Node):
    def __init__(self):
        super().__init__('segmentation')
        
        self.bridge = CvBridge()

        self.model = YOLO("yolo11n-seg.pt")

        self.subscription = self.create_subscription(
            Image,'/frames', self.process, 10)
        self.subscription 
        
        # self.video_path = "harder_challenge_video.mp4"
        # self.video_path = "challenge.mp4"
        
        # self.cap = cv2.VideoCapture(self.video_path)
        
        # self.timer = self.create_timer(0.1, self.process)

    def process(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        results = self.model(frame)
        
        annotated_frame = results[0].plot()
        
        cv2.imshow("Segmented Frame", annotated_frame)

    # def process(self):
    #     success, frame = self.cap.read()
        
    #     if success:
    #         results = self.model(frame)
    #         annotated_frame = results[0].plot()
    #         cv2.imshow("Segmented", annotated_frame)
    #         cv2.waitKey()
    #     else:
    #         self.cap.release()
    #         cv2.destroyAllWindows()
    #         rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = segmentation()
    rclpy.spin(node)
    # node.destroy_node()
    # rclpy.shutdown()

if __name__ == '__main__':
    main()