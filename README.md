# GestureController
## Requirements
- Python 3.7.9 (make sure its added to path)
- Dependences:
  ```
  pip install opencv-python
  pip install keyboard
  pip install psutil
  pip install keyboard
  pip install numpy
  pip install mediapipe
  pip install tensorflow
  pip install pywin32
  ```
## Pretrained model
The model we've generated is targeted to be used to control Spotify on Windows. Please see the diagram below;
![Spotify Gestures Diagram](https://github.com/Ivolutio/WebcamGestureController/blob/main/gestures.png?raw=true)

## Training your own model
Create a dataset folder with subfolders named with the gesture. E.g. `datasets/thumbsup`, `datasets/thumbsdown`.
Use the `take_pics.py` program to capture pictures of you performing the gesture by pressing `Q` on your keyboard.
The captures are saved in captures, simply put them in the correct dataset folder.
Now go to `train_model.py` and adjust the datasets property. 

```
datasets = [
  Dataset("neutral", 0),
  Dataset("thumbsup", 1),
  Dataset("thumbsdown", 2)
]
```
Headsup: Also train the model with enough `neutral` pictures of your hand doing someone unrelated to the gestures you want to use.
Then simply run the program and it will output a `model.h5` file. 
Now also update the datasets in the `posedetector.py`.

## Credits
- [@NeonChicken](https://github.com/NeonChicken)
  Research, model training, demonstration material
- [@Chyvex](https://github.com/Chyvex)
  Research and model training
- [@Ivolutio](https://github.com/Ivolutio)
  Research, programming

## Dev Notes
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
