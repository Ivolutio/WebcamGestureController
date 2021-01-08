# GestureController

## Notes
### HandLandmarks from MediaPipe
```python
# This is an enumerator for the idx of hand landmarks
from mediapipe.python.solutions.hands import HandLandmark

results = hands.process(image)
# For every hand found..
for hand_landmarks in results.multi_hand_landmarks:
  # idx = point
  # landmark = {
  #   visibility,
  #   presence,
  #   x, y (z)
  # }
  # landmark xy is 0 to 1 from left to right and top to bottom of the image
  for idx, landmark in enumerate(landmark_list.landmark):
    point_name = HandLandmark(idx).name #e.g. WRIST

    # Test which point
    if idx == HandLandmark.WRIST: 
      # ...
```