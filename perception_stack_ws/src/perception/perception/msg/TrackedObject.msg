# perception/msg/TrackedObject.msg
int32 track_id         # Unique ID for the tracked object
string class_name      # Class name (e.g., "person")
float32[4] bbox        # Bounding box [x1, y1, x2, y2]
