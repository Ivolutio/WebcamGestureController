import os
import numpy as np
import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
from mediapipe.python.solutions.hands import HandLandmark
import keyboard
import tensorflow as tf
from tensorflow import keras
import numpy as np

import processor

class Dataset:
  name: str
  category: int

  def __init__(self, name, category):
    self.name = name
    self.category = category

# Config
datasets = [
  Dataset("neutral", 0),
  Dataset("launch", 1),
  Dataset("play-pause", 2),
  Dataset("quit", 3),
  Dataset("track-next", 4),
  Dataset("track-prev", 5),
  Dataset("volume-down", 6),
  Dataset("volume-up", 7),
]

detection_threshold = 0.8

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
model = keras.models.load_model("model.h5")

def get_pose(image):
  detected_pose = datasets[0].name

  # Flip the image horizontally for a later selfie-view display, and convert
  # the BGR image to RGB.
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  image.flags.writeable = False
  results = hands.process(image)

  # Draw the hand annotations on the image.
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

  if results.multi_hand_landmarks:
    highestIndex = 0
    highestNr = 0
    for hand_landmarks in results.multi_hand_landmarks:
      data = processor.process_landmarks(image, hand_landmarks)
      predict = model.predict([data])
      strResults = str(predict[0]).replace("]", "").replace("[", "").split()
      for gesture in strResults:
        nr = float(gesture)
        if nr > highestNr:
          highestNr = nr
          highestIndex = strResults.index(gesture)

    if highestNr < detection_threshold:
      highestIndex = 0
    detected_pose = datasets[highestIndex].name
      
  # Show picture to user
  cv2.putText(image, detected_pose, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
  return detected_pose, image

# Flatten data
# data = []
# for finger in hand:
#   for point in finger:
#     data.append(point[0])
#     data.append(point[1])

# print(data)

# model = keras.models.load_model("model.h5")
# predict = model.predict([data])

# print(str(predict[0]))