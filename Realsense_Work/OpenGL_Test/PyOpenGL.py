#! /usr/bin/env python3



## Within this script, we will be able to inject the realsense coordinate information (hopefully)
## and then from there be able to localize a projection within our anybeam projector on to the wall
## localized to the realsense's reference frame

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (1370,720)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()

#include <GL/glut.h>
#include <math.h>
#include <iostream>
#include <librealsense2/rs.hpp>
'''
import PyOpenGL as gl

def displayMe(void):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT);
    gl.glColor3f(1.0, 0.0, 0.0);

    for i in range(8):
        for j in range(9):
            gl.glBegin(gl.GL_POLYGON);   
            radius = 0.01;
            ori_x = 0.0+0.051*j;                    
            ori_y = 0.1+0.1*i;
            for k in range(300):
                angle = 2 * 3.14159265 * i / 300;
                x = cos(angle) * radius;
                y = sin(angle) * radius *1280/720;
                gl.glVertex2d(ori_x + x, ori_y + y);
            
            gl.glEnd();

        
    gl.glFlush();

def main():
    gl.glutInit();
    gl.glutInitDisplayMode(gl.GLUT_SINGLE);
    gl.glutInitWindowSize(1280, 720);
    gl.glutInitWindowPosition(0, 0);
    gl.glutCreateWindow("Test 1: Display Triangle");
    gl.glutDisplayFunc(displayMe);
    gl.glutMainLoop();
'''