# LUS_MQP
This is my research done for my MQP in python rather than c++.
The following repository holds the work for my Major Qualifying Project to develop additions to the Lung Ultrasound (LUS) project pursued in the 
previous scholastic year by Fusion Labs. This addition to the LUS project will include 3D projection mapping augmentation as well as Long Term 
Support (LTS) implementation within the existing object detection library used in the previous year. 3D projection mapping is the projection of 
light onto a 3D object(s) that matches and/or compliments that object's contours in such a way where it looks like a blanket or mesh. In the case 
of this project, the 3D projection mapping in use will also take the pose estimation of an individual and live render its projection onto that 
individual if they were to move positions. It is expected that the work previously done on the project will interface the 3D projection mapping 
component in such a way where its detection points will have influence over the location of the projection. 

In recent years, Augmented Reality (AR) in the forms of wearable electronics (Hololens, realware) and non-wearable electronics (projection mapping) 
alike have gained massive popularity in the private sector (and massive “hype” in the public one). There will be continuous development on these 
technologies for the foreseeable future. One of the fields currently looking to implement these technologies for more than just marketing, art, 
or entertainment is the medical industry. There are an uncountable number of applications of AR in the medical industry. This project is meant to 
test and implement one of those applications. If successful, this method could go on to serve as a foundation for several other operations and use 
cases. 


## Setup
1. Make sure you are running the most recent version of Python 3.
2. Implement the PyOpenGL library software.
3. Implement the Detectron2 library software.
4. Implement the CV2 library software.
5. Clone the repository

## Running the environment
1. This project is supposed to be opened as the folder in VS code.
2. From there the directoruy in wich the project runs depends on which part of the project is being implemented.
  a. For the Realsense Work make sure that you are in this directory in the terminal to run any of the sub directories.
  b. For the Detectron Work, make sure you are in this directory in the terminal to run any of the sub directories.
