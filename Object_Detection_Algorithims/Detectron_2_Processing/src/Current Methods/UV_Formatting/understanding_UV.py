import numpy
import cv2
import matplotlib.pyplot as plt
import numpy as np

im  = cv2.imread('/home/medfuslab/Documents/GitHub/LUS_MQP/Object_Detection_Algorithims/Detectron_2/DensePoseData/Randy.jpg')
IUV = cv2.imread('/home/medfuslab/Documents/GitHub/LUS_MQP/Object_Detection_Algorithims/Detectron_2_Processing/results/densepose_contour.0001.png')

fig = plt.figure(figsize=[12,12])
plt.imshow( im[:,:,::-1] )
plt.contour(IUV[:,:,1]/256.,10, linewidths = 1 )
plt.contour(IUV[:,:,2]/256.,10, linewidths = 1 )

fig = plt.figure(figsize=[15,15])
plt.imshow(   np.hstack((IUV[:,:,0]/24. ,IUV[:,:,1]/256. ,IUV[:,:,2]/256.))  )
plt.title('I, U and V images.')
plt.axis('off') 
plt.show()

