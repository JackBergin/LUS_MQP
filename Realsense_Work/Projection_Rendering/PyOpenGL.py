#! /usr/bin/env python3

#Within this script, we will be able to inject the realsense coordinate information (hopefully)
#and then from there be able to localize a projection within our anybeam projector on to the wall
#localized to the realsense's reference frame


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import csv
from cv2 import pointPolygonTest

from regex import F

def plot_Point():
    #This function will plot a point in the center of the screen
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0,1.0,0.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glVertex2f(0.0, 0.0)
    glEnd()
    glFlush()

def clearScreen():
    #This function will flush out the screen from prior graphics
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1.0, 1.0,-1.0,1.0)

def getCalibrationPoints():
    #This function will read the calibration points/points of interest from subject
    id = []
    x = []
    y = []
    with open('Realsense_Work/Projection_Rendering/calibratedWorkSpace.csv', 'r') as csvfile:
        f = csv.reader(csvfile, delimiter = ',')
        for row in f:
            id.append(row[0])
            x.append(row[1])
            y.append(row[2])
    
    #Data cleaning portion
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

def convertCalibrationPoints():
    id, x, y = getCalibrationPoints()
    print(id)
    print(x)
    print(y)


def main():
    
    convertCalibrationPoints()
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(1370, 720)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Point")
    glutDisplayFunc(plot_Point)
    glTranslated(0,0,0.0)
    clearScreen()
    glutMainLoop()

main()
