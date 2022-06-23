#! /usr/bin/env python3

# import the necessary packages
import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
 
filename = "ArucoTest_Color"
frame = cv2.imread('Realsense_Work/ArUCo_Detection/image/'+filename+'.png')
plt.figure()
plt.imshow(frame)
plt.show()
 
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

print('Corners: ')
print(corners)
print(type(corners))
 
p = []
 
# verify *at least* one ArUco marker was detected
if len(corners) > 0:
 # flatten the ArUco IDs list
 ids = ids.flatten()
 # loop over the detected ArUCo corners
 for (markerCorner, markerID) in zip(corners, ids):
   # extract the marker corners (which are always returned in
   # top-left, top-right, bottom-right, and bottom-left order)
   corners = markerCorner.reshape((4, 2))
   (topLeft, topRight, bottomRight, bottomLeft) = corners
   # convert each of the (x, y)-coordinate pairs to integers
   topRight = (int(topRight[0]), int(topRight[1]))
   bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
   bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
   topLeft = (int(topLeft[0]), int(topLeft[1]))
 
   # draw the bounding box of the ArUCo detection
   cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
   cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
   cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
   cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
   # compute and draw the center (x, y)-coordinates of the ArUco
   # marker
   cX = int((topLeft[0] + bottomRight[0]) / 2.0)
   cY = int((topLeft[1] + bottomRight[1]) / 2.0)
   cY = int((topLeft[1] + bottomRight[1]) / 2.0)
 
   my_string = str((markerID, cX, cY))
   my_list = my_string.split(",")
   #my_string = str((markerID, cX, cY))
   print(my_list)
   p.append(my_list)
   cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
   # draw the ArUco marker ID on the frame
   cv2.putText(frame, str(markerID),
     (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
     0.5, (0, 255, 0), 2)
   print("[INFO] ArUco marker ID: {}".format(markerID))
   # show the output frame
   cv2.imwrite('Realsense_Work/ArUCo_Detection/type' + str(filename) + '_det.png', frame)
 plt.imshow(frame_markers)
print(p)
p = np.array(p)
p = p.reshape((len(ids), 3))
print(p.shape)
print(p)
np.save(str(filename) + '.npy', p)

