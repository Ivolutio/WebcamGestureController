import math
import enum
from typing import List, Tuple, Union
import cv2

import tensorflow as tf
from tensorflow import keras
import numpy as np
# import matpotlib.pyplot as plt


def map(x, in_min, in_max, out_min, out_max): 
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class HandLandmark(enum.IntEnum):
  """The 21 hand landmarks."""
  WRIST = 0
  THUMB_MCP = 1
  THUMB_PIP = 2
  THUMB_DIP = 3
  THUMB_TIP = 4
  INDEX_FINGER_MCP = 5
  INDEX_FINGER_PIP = 6
  INDEX_FINGER_DIP = 7
  INDEX_FINGER_TIP = 8
  MIDDLE_FINGER_MCP = 9
  MIDDLE_FINGER_PIP = 10
  MIDDLE_FINGER_DIP = 11
  MIDDLE_FINGER_TIP = 12
  RING_FINGER_MCP = 13
  RING_FINGER_PIP = 14
  RING_FINGER_DIP = 15
  RING_FINGER_TIP = 16
  PINKY_MCP = 17
  PINKY_PIP = 18
  PINKY_DIP = 19
  PINKY_TIP = 20

class Point: 
  name: str
  x: float
  y: float

  px: Union[None, Tuple[int, int]]
  _pxWidth: int
  _pxHeight: int

  # origin: Point = None

  @staticmethod
  def _normalized_to_pixel_coordinates(
      normalized_x: float, normalized_y: float, image_width: int,
      image_height: int) -> Union[None, Tuple[int, int]]:
    """Converts normalized value pair to pixel coordinates."""

    # Checks if the float value is between 0 and 1.
    def is_valid_normalized_value(value: float) -> bool:
      return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                        math.isclose(1, value))

    if not (is_valid_normalized_value(normalized_x) and
            is_valid_normalized_value(normalized_y)):
      # TODO: Draw coordinates even if it's outside of the image bounds.
      return None
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px

  def __init__(self, name: str, x: float, y: float, pxWidth: int, pxHeight: int):
    self.name = name
    self.x = x
    self.y = y

    self._pxWidth = pxWidth
    self._pxHeight = pxHeight

    self.px = self._normalized_to_pixel_coordinates(x, y, pxWidth, pxHeight)

    self.origin = None

  def draw(self, image, radius=1, color=(0, 255, 0)):
    cv2.circle(image, self.px, radius, color, -1)

  def make_relative(self, origin):
    if not self.origin:
      self.origin = origin
      self.x -= origin.x
      self.y -= origin.y
      # self.px = self._normalized_to_pixel_coordinates(self.x, self.y, self._pxWidth, self._pxHeight)    
    else:
      print("Origin already set")

  def get_data(self):
    return [self.x, self.y]

# Finger class, contains 4 points
class Finger: 
  name: str = "Unknown Finger"
  mcp: Point = None
  pip: Point = None
  dip: Point = None
  tip: Point = None

  color: Tuple[int,int,int] = (255, 0, 0)
  thickness: int = 1

  origin: Point = None

  def __init__(self, name, color=None, thickness=None):
    self.name = name
    if color: 
      self.color = color
    if thickness: 
      self.thickness = thickness
  
  def draw(self, image, color=None, thickness=None, drawPoints=False):
    if not color:
      color = self.color
    if not thickness:
      thickness = self.thickness

    if self.mcp.px and self.pip.px:
      cv2.line(image, self.mcp.px, self.pip.px, color, thickness)

    if self.pip.px and self.dip.px:
      cv2.line(image, self.pip.px, self.dip.px, color, thickness)
      
    if self.dip.px and self.tip.px:
      cv2.line(image, self.dip.px, self.tip.px, color, thickness)

    if drawPoints:
      if self.mcp:
        self.mcp.draw(image)
      if self.pip:
        self.pip.draw(image)
      if self.dip:
        self.dip.draw(image)
      if self.tip:
        self.tip.draw(image)

  def make_relative(self, origin: Point):
    self.origin = origin
    self.mcp.make_relative(origin)
    self.pip.make_relative(origin)
    self.dip.make_relative(origin)
    self.tip.make_relative(origin)

  def get_data(self):
    return [
      self.mcp.get_data(), 
      self.pip.get_data(),
      self.dip.get_data(),
      self.tip.get_data(),
    ]

class Hand:
  wrist: Point
  thumb: Finger
  index_finger: Finger
  middle_finger: Finger
  ring_finger: Finger
  pinky: Finger

  def __init__(self, wrist, thumb, index_finger, middle_finger, ring_finger, pinky):
    self.wrist = wrist

    self.thumb = thumb
    self.index_finger = index_finger
    self.middle_finger = middle_finger
    self.ring_finger = ring_finger
    self.pinky = pinky

    # self.thumb.make_relative(self.wrist)
    # self.index_finger.make_relative(self.wrist)
    # self.middle_finger.make_relative(self.wrist)
    # self.ring_finger.make_relative(self.wrist)
    # self.pinky.make_relative(self.wrist)

  def draw(self, image):
    self.wrist.draw(image, 2, (0,0,0))
    self.thumb.draw(image, (255,0,255))
    self.index_finger.draw(image, (0,0,255))
    self.middle_finger.draw(image, (0,255,0))
    self.ring_finger.draw(image, (255,0,0))
    self.pinky.draw(image, (0,255,255))

  def get_data(self):
    return [
      # self.wrist.get_data(),
      self.thumb.get_data(),
      self.index_finger.get_data(),
      self.middle_finger.get_data(),
      self.ring_finger.get_data(),
      self.pinky.get_data(),
    ]

  def get_coords(self):
    allPointsPerFinger = self.get_data()
    allCoords = []
    for finger in allPointsPerFinger:
      for point in finger:
        for coord in point:
          allCoords.append(coord)
    # print(allCoords)

    minX = 1
    minY = 1
    maxX = 0
    maxY = 0
    # go through each x and y, save min and max
    for coordIndex in range(0, len(allCoords), 2):
      x = allCoords[coordIndex]
      y = allCoords[coordIndex + 1]
      if x < minX:
        minX = x
      if x > maxX:
        maxX = x
      if y < minY:
        minY = y
      if y > maxY:
        maxY = y
    
    # print('minX', minX, 'maxX', maxX)
    # print('minY', minY, 'maxY', maxY)
    relativeCoords = []
    for coordIndex in range(0, len(allCoords), 2):
      x = map(allCoords[coordIndex], minX, maxX, 0, 1)
      y = map(allCoords[coordIndex + 1], minY, maxY, 0, 1)
      relativeCoords.append(x)
      relativeCoords.append(y)
    return relativeCoords


  @staticmethod
  def _normalized_to_pixel_coordinates(
      normalized_x: float, normalized_y: float, image_width: int,
      image_height: int) -> Union[None, Tuple[int, int]]:
    """Converts normalized value pair to pixel coordinates."""

    # Checks if the float value is between 0 and 1.
    def is_valid_normalized_value(value: float) -> bool:
      return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                        math.isclose(1, value))

    if not (is_valid_normalized_value(normalized_x) and
            is_valid_normalized_value(normalized_y)):
      # TODO: Draw coordinates even if it's outside of the image bounds.
      return None
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px

class FingerId(enum.IntEnum):
  THUMB = 0
  INDEX_FINGER = 1
  MIDDLE_FINGER = 2
  RING_FINGER = 3
  PINKY = 4

def process_landmarks(image, landmarks):
  if not landmarks:
    return

  image_rows, image_cols, _ = image.shape

  wrist = None
  fingers = [
    Finger("THUMB" , (0, 255, 0)), 
    Finger("INDEX" , (255, 255, 0)), 
    Finger("MIDDLE", (0, 0, 255)), 
    Finger("RING"  , (0, 255, 255)), 
    Finger("PINKY" , (255, 0, 255))
  ]

  # For each landmark found...
  for idx, landmark in enumerate(landmarks.landmark):
    # Only process visible landmarks 
    if landmark.visibility < 0 or landmark.presence < 0:
      continue
    
    # Create point object
    pointName = HandLandmark(idx).name
    point = Point(pointName, landmark.x, landmark.y, image_cols, image_rows)

    # Insert point at the right Finger object
    for i in range(5):
      fingerName = FingerId(i).name
      if fingerName in pointName:
        partName = pointName.split("_")[-1]
        if partName == "MCP":
          fingers[i].mcp = point
        elif partName == "PIP":
          fingers[i].pip = point
        elif partName == "DIP":
          fingers[i].dip = point
        elif partName == "TIP":
          fingers[i].tip = point
      elif pointName == "WRIST":
        wrist = point
  
  # Create hand
  hand = Hand(wrist, fingers[0], fingers[1], fingers[2], fingers[3], fingers[4])
  hand.draw(image)
  # hand.make_relative(image)

  return hand.get_coords()

def train_model(train_data, train_solutions):
  # train_data should be an array of hands
  # train_solutions should represent a label to a hand

  # model = keras.Sequential([
  #   keras.layers.Flatten(input_shape=(5, 4, 2))
  #   keras.layers.Dense(10, activation='relu')
  #   keras.layers.Dense(5, activation='softmax')
  # ])

  # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

  # Train the model
  # model.fit(train_data, train_solutions, epochs=10)

  # print("\n")
  pass


