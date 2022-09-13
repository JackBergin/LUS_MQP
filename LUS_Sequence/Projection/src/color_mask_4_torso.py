#!/usr/bin/env python

import numpy as np
import cv2
import csv
import matplotlib.pyplot as plt

frame = cv2.imread('LUS_Sequence/Detectron2/DensePoseData/densepose_segment.0001.png')

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#Blue Color
blue_light=np.array([99,115,150],np.uint8)
blue_dark=np.array([120,255,255],np.uint8)

#Creates mask based off of the blue range
mask = cv2.inRange(hsv, blue_light, blue_dark)
#Illustrates the mask being applied
res = cv2.bitwise_and(frame, frame, mask=mask)
#Takes the greyscale image and creates non-zero binaries around it
img = mask.astype(np.uint8)

#Gets all non zero values
coord = cv2.findNonZero(img)

x = []
y= []
print(coord[0])
for i in range(len(coord)):
    #Isolates to [[x,y]]
    parser = coord[i]
    #Isolates to [x,y]
    parser2 = parser[0]
    #Isolates to x,y
    x.append(parser2[0])
    y.append(parser2[1])


plt.figure(1)
plt.plot(x, y, 'o', color='black');
plt.xlabel('X', fontsize = 10)
plt.ylabel('Y', fontsize = 10)
ax = plt.gca()
ax.invert_yaxis()
plt.title('Body Segmentation Visualization', fontsize = 20)
plt.show()

cv2.imwrite('LUS_Sequence/Projection/src/results/frame.png', frame)
cv2.imwrite('LUS_Sequence/Projection/src/results/hsv.png', hsv)
cv2.imwrite('LUS_Sequence/Projection/src/results/mask.png', mask)
cv2.imwrite('LUS_Sequence/Projection/src/results/res.png', res)