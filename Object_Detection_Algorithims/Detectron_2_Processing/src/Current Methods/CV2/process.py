from re import M
import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt

path = '/home/medfuslab/Documents/GitHub/LUS_MQP/Object_Detection_Algorithims/Detectron_2_Processing/results/densepose_u.0001.png'
image = cv2.imread(path)

#gray = cv2.cvtColor(image, cv2.COLOR_BGR2XYZ )

kernel = np.ones((5, 5), np.uint8)
modifiedImg = cv2.erode(image, kernel, cv2.BORDER_REFLECT)
modifiedImg = cv2.erode(image, kernel, cv2.BORDER_REFLECT)

modifiedImg = cv2.dilate(image, kernel, iterations=5)

subtracted = np.subtract(modifiedImg, image)
combined = cv2.dilate(subtracted, kernel, iterations = 5)

cv2.imwrite('/home/medfuslab/Documents/GitHub/LUS_MQP/Object_Detection_Algorithims/Detectron_2_Processing/processed_imgs/original.png',image)
cv2.imwrite('/home/medfuslab/Documents/GitHub/LUS_MQP/Object_Detection_Algorithims/Detectron_2_Processing/processed_imgs/modified.png', modifiedImg)
cv2.imwrite('/home/medfuslab/Documents/GitHub/LUS_MQP/Object_Detection_Algorithims/Detectron_2_Processing/processed_imgs/subtracted.png', subtracted)

params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 1000
params.filterByColor = True
params.filterByArea = False
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False

detector = cv2.SimpleBlobDetector_create(params)
detector.empty()
keypoint = detector.detect(combined)

detected_Torso = cv2.drawKeypoints(modifiedImg, keypoint, np.array([]), (0, 160, 160), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imwrite('/home/medfuslab/Documents/GitHub/LUS_MQP/Object_Detection_Algorithims/Detectron_2_Processing/processed_imgs/detected_Torso.png', detected_Torso)

#https://stackoverflow.com/questions/42924059/detect-different-color-blob-opencv

## Cool idea for segmentation of the detected area for fronteir detection?
# https://realpython.com/python-opencv-color-spaces/

# Reads the image of vcoord
vcoord = cv2.imread('/home/medfuslab/Documents/GitHub/LUS_MQP/Object_Detection_Algorithims/Detectron_2_Processing/results/densepose_v.0001.png')

#Converts to the hsv range from rgb
hsv_vcoord = cv2.cvtColor(vcoord, cv2.COLOR_RGB2HSV)


h, s, v = cv2.split(hsv_vcoord)
pixel_colors = vcoord.reshape((np.shape(vcoord)[0]*np.shape(vcoord)[1],3))
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")

axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Hue")
axis.set_ylabel("Saturation")
axis.set_zlabel("Value")
plt.show()


'''
# Creates masking range
dark_yellow = (52, 84, 100)
light_yellow = (60, 68, 100)
mask = cv2.inRange(hsv_vcoord, light_yellow, dark_yellow)
result = cv2.bitwise_and(vcoord, vcoord, mask=mask)

plt.subplot(1, 2, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()
'''