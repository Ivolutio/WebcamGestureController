import enum
import numpy as np
import cv2

import mediapipe as mp
mp_hands = mp.solutions.hands
from mediapipe.python.solutions.hands import HandLandmark

import keyboard
from datetime import datetime
import time

import processor

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

qPressed = False

cap = cv2.VideoCapture(0)
while cap.isOpened():
  success, image = cap.read()
  if not success:
    break

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
    # When q is pressed, take a picture
    if keyboard.is_pressed('q') and not qPressed:
      qPressed = True
      now = str(int(round(time.time() * 1000)))
      print(now)
      cv2.imwrite("captures/" +  now + ".jpg", image)
      print("take capture")
    if not keyboard.is_pressed('q') and qPressed:
      # This will make sure the take_picture command only fires once
      qPressed = False

    # Draw hands    
    for hand_landmarks in results.multi_hand_landmarks:
      processor.process_landmarks(image, hand_landmarks)

  # Show picture to user
  cv2.imshow('MediaPipe Hands', image)

  # Stop program when 'x' key is pressed
  if keyboard.is_pressed('x') & cv2.waitKey(1):
    break

hands.close()
cap.release()