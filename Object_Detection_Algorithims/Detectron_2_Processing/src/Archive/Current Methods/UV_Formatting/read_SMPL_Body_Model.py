from asyncio.windows_events import NULL
import densepose_methods as dp_utils
import numpy as np
import cv2 as cv2
DP = dp_utils.DensePoseMethods()
import time

pick_idx = 1    # PICK PERSON INDEX!

#Current place holder because the current way things are working in Detectron2 instance disinclude the INDS filter
INDS = NULL
IUV = cv2.imread('/home/medfuslab/Documents/GitHub/LUS_MQP/Object_Detection_Algorithims/Detectron_2_Processing/results/densepose_contour.0001.png')

C = np.where(INDS == pick_idx)
# C[0] is x-coords  np.array([23,  23,   24, ..])
# C[1] is y-coords  np.array([127, 128, 130, ..])
print('num pts on picked person:', C[0].shape)
IUV_pick = IUV[C[0], C[1], :]  # boolean indexing
IUV_pick = IUV_pick.astype(np.float)
IUV_pick[:, 1:3] = IUV_pick[:, 1:3] / 255.0
print(IUV_pick.shape)
collected_x = np.zeros(C[0].shape)
collected_y = np.zeros(C[0].shape)
collected_z = np.zeros(C[0].shape)