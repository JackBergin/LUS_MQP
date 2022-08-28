#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: color-filter.py

import numpy as np
import cv2


frame = cv2.imread('Object_Detection_Algorithims/Detectron_2_Processing/results/densepose_segment.0001.png')

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Blue Color
blue_light=np.array([99,115,150],np.uint8)
blue_dark=np.array([120,255,255],np.uint8)

mask = cv2.inRange(hsv, blue_light, blue_dark)
res = cv2.bitwise_and(frame, frame, mask=mask)

cv2.imwrite('Object_Detection_Algorithims/Detectron_2_Processing/src/Current Methods/CV2/results/frame.png', frame)
cv2.imwrite('Object_Detection_Algorithims/Detectron_2_Processing/src/Current Methods/CV2/results/hsv.png', hsv)
cv2.imwrite('Object_Detection_Algorithims/Detectron_2_Processing/src/Current Methods/CV2/results/mask.png', mask)
cv2.imwrite('Object_Detection_Algorithims/Detectron_2_Processing/src/Current Methods/CV2/results/res.png', res)

#cv2.destroyAllWindows()