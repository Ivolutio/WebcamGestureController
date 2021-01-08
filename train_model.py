import os
import numpy as np
import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
from mediapipe.python.solutions.hands import HandLandmark
import keyboard
import processor
import tensorflow as tf
from tensorflow import keras
import numpy as np

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

# Setup hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Result data array
train_data = []
train_solutions = []

# Go through all given datasets
for dataset in datasets:

  # Go through each file in the selected dataset directory
  directory = os.fsencode("./datasets/" + dataset.name)
  for file in os.listdir(directory):
    filename = "./datasets/" + dataset.name + "/" + os.fsdecode(file)
    if filename.endswith(".jpg"): 
      # Open file
      image = cv2.imread(filename)
      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
      image.flags.writeable = False

      results = hands.process(image)

      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          train_data.append(processor.process_landmarks(image, hand_landmarks))
          train_solutions.append(dataset.category)
        print(filename)
      else:
        print("no hands found in", filename)
        # os.remove(filename)

# print(train_results)

# train_data should be an array of hands
# train_solutions should represent a label to a hand

model = keras.Sequential([
  keras.layers.Dense(40, activation='relu'),
  keras.layers.Dense(15, activation='relu'),
  keras.layers.Dense(8, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

# # Train the model
model.fit(train_data, train_solutions, epochs=10)

model.save('model.h5')

# print("\n")
hands.close()