#! /usr/bin/env python3

# import the necessary packages
import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
 
filename = "RGB-Img-Test-1"
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
 

#This next part will require the parsing of the detected ArUCo Markers to create bounds
print(corners[0])