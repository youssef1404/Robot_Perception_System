import sys
sys.path.append('src/perception/perception/')

from perception.deep_sort.deep_sort.tracker import Tracker as DeepSortTracker
from perception.deep_sort.tools import generate_detections as gdet
from perception.deep_sort.deep_sort import nn_matching
from perception.deep_sort.deep_sort.detection import Detection
import numpy as np
import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "artifacts/mars-small128.pb")



class Tracker:
    tracker = None # An instance of the Deep SORT tracker.
    encoder = None # A neural network-based feature encoder to create feature vectors from detected objects.
    tracks = None # A list of active tracked objects.
    class_name_map = None  # Dictionary to persist class names per track ID

    def __init__(self):
        max_cosine_distance = 0.4
        nn_budget = None

        ## Loads the feature extraction model (mars-small128.pb), which is used to encode object appearances.
        encoder_model_filename = os.path.join(os.path.dirname(__file__), "artifacts/mars-small128.pb")



        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.tracker = DeepSortTracker(metric)
        self.encoder = gdet.create_box_encoder(encoder_model_filename, batch_size=1)
        self.class_name_map = {} 

    def update(self, frame, detections, class_names=None):
        """Update tracker with detections and optional class names."""
        if len(detections) == 0:
            self.tracker.predict()
            self.tracker.update([])  
            self.update_tracks()
            return

        bboxes = np.asarray([d[:-1] for d in detections])
        bboxes[:, 2:] = bboxes[:, 2:] - bboxes[:, 0:2] # Converts bounding box coordinates from [x1, y1, x2, y2] to [x, y, width, height].
        scores = [d[-1] for d in detections]

        # Ensure class_names matches detections length, or default to None
        if class_names is None or len(class_names) != len(detections):
            class_names = [None] * len(detections)

        # Uses the feature extraction model (self.encoder) to generate deep feature vectors for detected objects.
        features = self.encoder(frame, bboxes)

        dets = []
        for bbox_id, bbox in enumerate(bboxes):
            dets.append(Detection(bbox, scores[bbox_id], features[bbox_id]))

        self.tracker.predict() # to estimate object movement.
        self.tracker.update(dets) # which matches detections with existing tracks or initializes new ones.
        self.update_tracks(class_names) # to refresh the tracks list.

    def update_tracks(self, class_names=None):
        """Update the list of active tracks with persistent class names."""
        tracks = []
        for i, track in enumerate(self.tracker.tracks):
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()
            track_id = track.track_id

            # Persist class name: use existing name if already assigned, otherwise set new one
            if track_id not in self.class_name_map and class_names and i < len(class_names) and class_names[i]:
                self.class_name_map[track_id] = class_names[i]
            class_name = self.class_name_map.get(track_id, "Unknown")

            tracks.append(Track(track_id, bbox, class_name))

        self.tracks = tracks


class Track:
    track_id = None
    bbox = None
    class_name = None  

    def __init__(self, id, bbox, class_name=None):
        self.track_id = id
        self.bbox = bbox
        self.class_name = class_name  
