#! /usr/bin/env python3

#Within this script, we will be able to inject the realsense coordinate information (hopefully)
#and then from there be able to localize a projection within our anybeam projector on to the wall
#localized to the realsense's reference frame


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def plot_Point():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0,1.0,0.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glVertex2f(0.0, 0.0)
    glEnd()
    glFlush()

def clearScreen():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1.0, 1.0,-1.0,1.0)

def main():
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
