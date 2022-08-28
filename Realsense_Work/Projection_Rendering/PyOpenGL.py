#! /usr/bin/env python3

# Within this script, we will be able to inject the realsense coordinate information (hopefully)
# and then from there be able to localize a projection within our anybeam projector on to the wall
# localized to the realsense's reference frame


from cmath import nan
from time import sleep
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import csv
from cv2 import pointPolygonTest
from numpy import NAN

#from regex import F

def plot_Point():
    # This function will plot a point in the center of the screen
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0,1.0,0.0)
    glPointSize(5.0)
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
    with open('Realsense_Work/Projection_Rendering/calibratedWorkSpace.csv', 'r') as csvfile:
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

def convertCalibrationPoints(imageCoordX, imageCoordY):
    id, x, y = getCalibrationPoints()

    minXBound = min(x)
    minYBound = min(y)
    maxXBound = max(x)
    maxYBound = max(y)
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

def main():
    #Calling transform method
    xPoint, yPoint, maxXBound, maxYBound, minXBound, minYBound = convertCalibrationPoints(316, 270) #10
    x1Point, y1Point, maxXBound, maxYBound, minXBound, minYBound = convertCalibrationPoints(313, 220) #9
    x2Point, y2Point, maxXBound, maxYBound, minXBound, minYBound = convertCalibrationPoints(319, 322) #11
    x3Point, y3Point, maxXBound, maxYBound, minXBound, minYBound = convertCalibrationPoints(367, 268) #6
    x4Point, y4Point, maxXBound, maxYBound, minXBound, minYBound = convertCalibrationPoints(364, 217) #5
    x5Point, y5Point, maxXBound, maxYBound, minXBound, minYBound = convertCalibrationPoints(423, 317) #3
    x6Point, y6Point, maxXBound, maxYBound, minXBound, minYBound = convertCalibrationPoints(419, 265) #2
    x7Point, y7Point, maxXBound, maxYBound, minXBound, minYBound = convertCalibrationPoints(416, 214) #1


    #Casting to integers
    xSizeOfScreen = int(maxXBound+minXBound)
    ySizeOfScreen = int(maxYBound+minYBound)
    xStartingPoint = int(maxXBound)
    yStartingPoint = int(maxYBound)
    
    #Debug prints
    print("Current Screen Size:")
    print(xSizeOfScreen)
    print(ySizeOfScreen)
    print()
    print("Bounds:")
    print(maxXBound)
    print(maxYBound)
    print(minXBound)
    print(minYBound)
    print()
    print("Location of Screen:")
    print(xStartingPoint)
    print(yStartingPoint)
    

    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(round(xSizeOfScreen*1.525), round(ySizeOfScreen*1.015))
    glutInitWindowPosition(round(xStartingPoint*1.14), round(yStartingPoint*0.225))
    glutCreateWindow("Point")
    glutDisplayFunc(plot_Point)
    '''
    Tested Points:
    glTranslated(xPoint,yPoint,0.0)
    clearScreen()
    '''
    

    glTranslated(x1Point,y1Point,0.0)
    clearScreen()
    '''

    glTranslated(x2Point,y2Point,0.0)
    sleep(1)
    clearScreen()
    glTranslated(x3Point,y3Point,0.0)
    sleep(1)
    clearScreen()
    glTranslated(x4Point,y4Point,0.0)
    sleep(1)
    clearScreen()
    glTranslated(x5Point,y5Point,0.0)
    sleep(1)
    clearScreen()
    glTranslated(x6Point,y6Point,0.0)
    sleep(1)
    clearScreen()
    glTranslated(x7Point,y7Point,0.0)
    '''
    glutMainLoop()

main()
