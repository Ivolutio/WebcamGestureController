import cv2
import keyboard
import posedetector

pose_ignore = 'neutral'
duration_threshold = 20

curr_pose = ''
curr_pose_duration = 0

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
      print("Activate", pose)
  else: 
    curr_pose = pose
    curr_pose_duration = 0

  cv2.putText(image, str(curr_pose_duration), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)

  cv2.imshow('Spotify Controller', image)

  # Stop program when 'x' key is pressed
  if keyboard.is_pressed('x') & cv2.waitKey(1):
    break

cap.release()