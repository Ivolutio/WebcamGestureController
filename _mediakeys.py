import cv2
import keyboard
import os
import psutil
import win32api
from win32con import VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, VK_MEDIA_PREV_TRACK, VK_VOLUME_DOWN, VK_VOLUME_UP, KEYEVENTF_EXTENDEDKEY

import posedetector

pose_ignore = 'neutral'
duration_threshold = 20

curr_pose = ''
curr_pose_duration = 0

def kill_app(name):
  for proc in psutil.process_iter():
    if proc.name() == name:
      proc.kill()

# Activate code from pose names
# https://docs.microsoft.com/uk-ua/windows/win32/inputdev/virtual-key-codes
def process_pose(pose):
  print("Activate", pose)
  if pose == "play-pause":
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
  elif pose == 'track-next':
    win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)
  elif pose == 'track-prev':
    win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)
  elif pose == 'volume-down':
    win32api.keybd_event(VK_VOLUME_DOWN, 0, KEYEVENTF_EXTENDEDKEY, 0)
  elif pose == 'volume-up':
    win32api.keybd_event(VK_VOLUME_UP, 0, KEYEVENTF_EXTENDEDKEY, 0)
    
  elif pose == "launch":
    os.startfile(os.getcwd() + "\spotify.lnk")
  elif pose == "quit":
    kill_app("Spotify.exe")

# Main loop
cap = cv2.VideoCapture(0)
while cap.isOpened():
  success, image = cap.read()
  if not success:
    break


  pose, image = posedetector.get_pose(image)

  if pose == curr_pose and pose != pose_ignore:
    curr_pose_duration += 1
    if curr_pose_duration > duration_threshold:
      curr_pose_duration = 0
      process_pose(pose)
  else: 
    curr_pose = pose
    curr_pose_duration = 0

  cv2.putText(image, str(curr_pose_duration), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)

  cv2.imshow('Spotify Controller', image)

  # Stop program when 'x' key is pressed
  if keyboard.is_pressed('x') & cv2.waitKey(1):
    break

cap.release()

