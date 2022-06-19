#! /usr/bin/env python3



## Within this script, we will be able to inject the realsense coordinate information (hopefully)
## and then from there be able to localize a projection within our anybeam projector on to the wall
## localized to the realsense's reference frame

#include <GL/glut.h>
#include <math.h>
#include <iostream>
#include <librealsense2/rs.hpp>

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
