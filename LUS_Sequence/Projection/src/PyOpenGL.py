#! /usr/bin/env python3

# Within this script, we will be able to inject the realsense coordinate information (hopefully)
# and then from there be able to localize a projection within our anybeam projector on to the wall
# localized to the realsense's reference frame

import sys
sys.path.append("/home/medfuslab/anaconda3/lib/python3.9/site-packages")

import subprocess
from cmath import nan
from time import sleep
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import csv
from cv2 import pointPolygonTest
from numpy import NAN
import RS_Read as rs
import color_mask_4_torso as mask

def plot_Point():
    # This function will plot a point in the center of the screen
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0,0.0,0.0)
    glPointSize(20.0)
    glBegin(GL_POINTS)
    glVertex2f(0.0, 0.0)
    glEnd()
    glFlush()

def clearScreen():
    # This function will flush out the screen from prior graphics
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1.0, 1.0,-1.0,1.0)

def getCalibrationPoints():
    # This function will read the calibration points/points of interest from subject
    id = []
    x = []
    y = []
    with open('LUS_Sequence/Projection/data/calibratedWorkSpace.csv', 'r') as csvfile:
        f = csv.reader(csvfile, delimiter = ',')
        for row in f:
            id.append(row[0])
            x.append(row[1])
            y.append(row[2])
    
    # Data cleaning portion
    id = [i.replace('(', '') for i in id]
    y = [i.replace(')', '') for i in y]
    y = [i.replace(' ', '') for i in y]    
    x = [i.replace(' ', '') for i in x]

    size = len(id)

    # Casts all values to float values from string
    floatID = []
    floatX = []  
    floatY = []
    for j in range(size):
        floatID.append(float(id[j]))
        floatX.append(float(x[j]))
        floatY.append(float(y[j]))

    return floatID, floatX, floatY

def getCornerPoints():
    x = []
    y = []
    with open('LUS_Sequence/Projection/data/arUCoCorners.csv', 'r') as csvfile:
        f = csv.reader(csvfile, delimiter = ',')
        for row in f:
            x.append(row[0])
            y.append(row[1])
    
    floatX = []  
    floatY = []
    for j in range(4):
        floatX.append(float(x[j]))
        floatY.append(float(y[j]))
    
    return floatX, floatY
    
def convertCalibrationPoints(imageCoordX, imageCoordY):
    xLim, yLim = getCornerPoints()

    minXBound = min(xLim)
    minYBound = min(yLim)
    maxXBound = max(xLim)
    maxYBound = max(yLim)
    averageX = ((maxXBound-minXBound)/2)+minXBound
    averageY = ((maxYBound-minYBound)/2)+minYBound
    
    print(averageX)
    print(averageY)

    if((minXBound < imageCoordX) and (imageCoordX < maxXBound)):
        if(imageCoordX < averageX):
            convertedXPoint = -1*(1-(imageCoordX-minXBound)/(averageX-minXBound))
        elif(imageCoordX > averageX):
            convertedXPoint = 1-(maxXBound-imageCoordX)/(maxXBound-averageX)
        else:
            convertedXPoint = 0
    else:
        print("Out of X range!")

    if((minYBound < imageCoordY) and (imageCoordY < maxYBound)):
        if(imageCoordY > averageY):
            convertedYPoint = -1-(imageCoordY-maxYBound)/(maxYBound-averageY)
        elif(imageCoordY < averageY):
            convertedYPoint = 1-(imageCoordY-minYBound)/(averageY-minYBound)
        else:
            convertedYPoint = 0
    else:
        print("Out of Y range!")
    
    #Debug prints
    print("Converted X Point:")
    print(convertedXPoint)
    print("Converted Y Point:")
    print(convertedYPoint)
    print()
    
    return convertedXPoint,convertedYPoint, maxXBound, maxYBound, minXBound, minYBound

def selectPoint(enteredID):
    id, x, y = getCalibrationPoints()
    for i in range(len(x)):
       if(id[i] == enteredID):
        return x[i],y[i]
       else: 
        return 0,0
        
def main():
    # Calls detectron2
    rs.main()
    filename = 'LUS_Sequence/Projection/detectron2/launchDetectron.sh'
    subprocess.call(['sh', './LUS_Sequence/Projection/detectron2/launchDetectron.sh'])
    
    detectronX = []
    detectronY = []
    detectronX, detectronY = mask.masking()

    # Calling transform method
    xPoint, yPoint, maxXBound, maxYBound, minXBound, minYBound = convertCalibrationPoints(327, 260)    

    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(1150,500)
    glutInitWindowPosition(320,100)
    glutCreateWindow("Point")
    glutDisplayFunc(plot_Point)
    
    #Tested Points:
    glTranslated(xPoint,yPoint,0.0)
    clearScreen()
    glutMainLoop()

main()
