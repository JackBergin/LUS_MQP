from curses.ascii import ETB
from shutil import SpecialFileError
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
from pyntcloud import PyntCloud # open source library for 3D pointcloud visualisation
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import csv

def main():
  print("Environment Ready")
  # Setup:
  hardware_reset_RS()
  pipe = rs.pipeline()
  pipe.start()
  pc = rs.pointcloud()
  exitLoop = True

  while exitLoop == True:
    frameset = pipe.wait_for_frames()

    color_frame = frameset.get_color_frame()   
    if (not color_frame):
      color_frame = frameset.get_infrared_frame()

    pc.map_to(color_frame)

    depth_frame = frameset.get_depth_frame()
    pointcloud = pc.calculate(depth_frame)
    size = pointcloud.size()
 
    print("Size: ", size) 

    # Collects the point cloud data and makes a list   
    vtx = np.asanyarray(pointcloud.get_vertices())
    
    # Parses though the list, removes all of the "empty" points 
    # and then adds the full points on a new clean list
    parseVTX = []
    correctedPointcloud = []

    for i in range(size):
      parseVTX = vtx[i]
      if parseVTX[2] == 0.0 or parseVTX[2] == -0.0:
        np.delete(vtx, i, 0)
      else:
        print("Position = ", i)
        print("Value = ", vtx[i])
        correctedPointcloud.append(vtx[i])

    
    # Writes the new cleaned list to a csv file
    with open('Projection_Rendering/fullPointCloud.csv', 'w') as f:
        writer = csv.writer(f)
        for i in range(correctedPointcloud.size()):
            writer.writerow(correctedPointcloud)
    

    # Loops if the pointcloud collection fails (tolerance in this case is over 10,000 points)
    if(pointcloud.size() > 10000):
       exitLoop = False
    else:
      exitLoop = True

# Hardware reset preformed for the connectivity of the Realsense to be maintained
def hardware_reset_RS():
    print("reset start")
    ctx = rs.context()
    devices = ctx.query_devices()
    for dev in devices:
        dev.hardware_reset()
    print("reset done")


main()