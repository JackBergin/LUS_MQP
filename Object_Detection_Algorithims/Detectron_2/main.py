import cv2 
from matplotlib import pyplot as plt

im_cont = cv2.imread("DensePoseData/densepose_contour.0001.png")
im_segm = cv2.imread("DensePoseData/densepose_segment.0001.png")
im_u = cv2.imread("DensePoseData/densepose_u.0001.png")
im_v = cv2.imread("DensePoseData/densepose_v.0001.png")

plt.rcParams["figure.figsize"]=20,20
plt.subplot(2,2,1)
plt.imshow(im_cont[:,:,::-1])
plt.axis('off')
plt.title('body contour')

plt.subplot(2,2,2)
plt.imshow(im_segm[:,:,::-1])
plt.axis('off')
plt.title('body segmentation')

plt.subplot(2,2,3)
plt.imshow(im_u[:,:,::-1])
plt.axis('off')
plt.title('u coordinates')

plt.subplot(2,2,4)
plt.imshow(im_v[:,:,::-1])
plt.axis('off')
plt.title('v coordinates')