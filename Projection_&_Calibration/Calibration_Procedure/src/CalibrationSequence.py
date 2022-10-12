#! /usr/bin/env python3

# import the necessary packages
import numpy as np
from cv2 import aruco
import matplotlib.pyplot as plt

import cv2 as cv2
from GetSurfaceNormal import *
from pyrealsense2 import pyrealsense2 as rs

import csv
'''
Get the necessary code for the Realsense to fill above the ArUCo tag work.
'''
class CalibrationSequence():
    __pipeline = rs.pipeline()
    __config = rs.config()

    def __init__(self):
        self.__config.enable_stream(
            rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.__config.enable_stream(
            rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # process
        self.__align_depth2color = rs.align(rs.stream.color)
        self.__pc = rs.pointcloud()   # get pointcloud
        # frame data
        self.depth_image = None
        self.depth_colormap = None
        self.depth_frame = None
        self.color_image = None
        self.color_frame = None
        self.verts = None           # xyz
        self.texcoords = None       # u,v
        # start streaming
        self.__pipeline.start(self.__config)
        # camera intrinsic
        self.__profile = self.__pipeline.get_active_profile()
        self.intr = self.__profile.get_stream(
            rs.stream.color).as_video_stream_profile().get_intrinsics()

    def __del__(self):
        self.__pipeline.stop()

    # ====================== interface ======================
    def stream_color_frame(self):
        frames = self.__pipeline.wait_for_frames()
        self.color_frame = frames.get_color_frame()
        if self.color_frame:
            # Convert images to numpy arrays
            self.color_image = np.asanyarray(self.color_frame.get_data())

    def stream_depth_frame(self):
        frames = self.__pipeline.wait_for_frames()
        self.depth_frame = frames.get_depth_frame()
        # apply depth filters
        self.depth_filter()
        if self.depth_frame:
            # Convert images to numpy arrays
            self.depth_image = np.asanyarray(self.depth_frame.get_data())
            self.depth_colormap = cv2.applyColorMap(
                cv2.convertScaleAbs(self.depth_image, alpha=0.03), cv2.COLORMAP_JET)

    def stream_depth2color_aligned(self):
        frames = self.__pipeline.wait_for_frames()
        # align depth to color frame
        aligned_frames = self.__align_depth2color.process(frames)
        self.depth_frame = aligned_frames.get_depth_frame()
        self.color_frame = aligned_frames.get_color_frame()
        # apply depth filters
        self.depth_filter()
        if self.depth_frame and self.color_frame:
            self.depth_image = np.asanyarray(self.depth_frame.get_data())
            self.depth_colormap = cv2.applyColorMap(
                cv2.convertScaleAbs(self.depth_image, alpha=0.03), cv2.COLORMAP_JET)
            self.color_image = np.asanyarray(self.color_frame.get_data())

    def stream_pointcloud(self):
        self.stream_depth2color_aligned()
        if self.depth_frame:
            points = self.__pc.calculate(self.depth_frame)
            self.__pc.map_to(self.depth_frame)
            # Pointcloud data to arrays
            v, t = points.get_vertices(), points.get_texture_coordinates()
            self.verts = np.asanyarray(v).view(
                np.float32).reshape(-1, 3)   # xyz
            self.texcoords = np.asanyarray(t).view(
                np.float32).reshape(-1, 2)  # uv

    # ====================== utility ======================
    def depth_filter(self):
        if self.depth_frame:
            self.depth_frame = rs.decimation_filter(
                1).process(self.depth_frame)
            self.depth_frame = rs.disparity_transform(
                True).process(self.depth_frame)
            self.depth_frame = rs.spatial_filter().process(self.depth_frame)
            self.depth_frame = rs.temporal_filter().process(self.depth_frame)
            self.depth_frame = rs.disparity_transform(
                False).process(self.depth_frame)

    def get_xyz(self, pixels: list, flatten_out=False) -> np.ndarray:
        '''
        get xyz points from pixels in depth frame
        '''
        depth_intrin = self.depth_frame.profile.as_video_stream_profile().intrinsics
        points = []
        for i in range(len(pixels)):
            pix = pixels[i]
            try:
                depth_in_met = self.depth_frame.as_depth_frame(
                ).get_distance(pix[1], pix[0])
                pnt = rs.rs2_deproject_pixel_to_point(
                    depth_intrin, pix, depth_in_met)
            except Exception as err:
                print(err)
                pnt = [-1, -1, -1]
            points.append(pnt)
        points_formatted = np.reshape(points, [len(pixels), 3])
        if flatten_out:
            points_formatted = np.array(points).flatten()
        return points_formatted

    def get_surface_normal(self, pixel: list) -> np.ndarray:
        '''
        given a pixel in 2D image, calculate normal vector
        '''
        patch = get_patch(pixel)
        points = self.get_xyz(patch)
        norm = get_surface_normal(points[:, 0], points[:, 1], points[:, 2])
        pos = points[0, :]
        return norm, pos

    def hardware_reset_RS(void):
        print("reset start")
        ctx = rs.context()
        devices = ctx.query_devices()
        for dev in devices:
            dev.hardware_reset()
        print("reset done")

if __name__ == "__main__":
    get_realsense_data = CalibrationSequence()
    get_realsense_data.hardware_reset_RS()
    cv2.namedWindow('RGB-depth', cv2.WINDOW_AUTOSIZE)
    while True:
        key = cv2.waitKey(10)
        if key & 0xFF == ord('Q') or key == 27:
            cv2.destroyAllWindows()
            break
        get_realsense_data.stream_depth2color_aligned()
        color_depth_stack = np.vstack(
            (get_realsense_data.color_image, get_realsense_data.depth_colormap))

        filename = 'Calibration1'
        cv2.imshow(str(filename), color_depth_stack)
        cv2.imwrite('Realsense_Work/Calibration_Procedure/image/calibrationImg.png', get_realsense_data.color_image)

        frame = cv2.imread('Realsense_Work/Calibration_Procedure/image/calibrationImg.png')
        plt.figure()
        
        plt.imshow(frame)
        plt.show()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        print('Corners: ')
        print(corners)
        print(type(corners))
        
        p = []
        addCorners = []
        # verify *at least* one ArUco marker was detected
        if len(corners) > 0:
        # flattefn the ArUco IDs list
         ids = ids.flatten()
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
          # extract the marker corners (which are always returned in
          # top-left, top-right, bottom-right, and bottom-left order)
          corners = markerCorner.reshape((4, 2))
          (topLeft, topRight, bottomRight, bottomLeft) = corners

          if(markerID == 1):
            addCorners.append(topLeft)
          elif(markerID == 2):
            addCorners.append(topRight)
          elif(markerID == 3):
            addCorners.append(bottomLeft)
          elif(markerID == 4):
            addCorners.append(bottomRight)
          else:
            print('Not a corner marker')
            print(markerID)

          # convert each of the (x, y)-coordinate pairs to integers
          topRight = (int(topRight[0]), int(topRight[1]))
          bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
          bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
          topLeft = (int(topLeft[0]), int(topLeft[1]))
        
          # draw the bounding box of the ArUCo detection
          cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
          cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
          cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
          cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
          # compute and draw the center (x, y)-coordinates of the ArUco
          # marker
          cX = int((topLeft[0] + bottomRight[0]) / 2.0)
          cY = int((topLeft[1] + bottomRight[1]) / 2.0)
          cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        
          my_string = str((markerID, cX, cY))
          my_list = my_string.split(",")
          #my_string = str((markerID, cX, cY))
          print(my_list)
          p.append(my_list)
          cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
          # draw the ArUco marker ID on the frame
          cv2.putText(frame, str(markerID),
            (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 255, 0), 2)
          print("[INFO] ArUco marker ID: {}".format(markerID))
          # show the output frame
          cv2.imwrite('Realsense_Work/Calibration_Procedure/type/calibration_det.png', frame)
        plt.imshow(frame_markers)
        print(p)
        p = np.array(p)
        p = p.reshape((len(ids), 3))
        print(p.size)
        
        with open('Realsense_Work/Projection_Rendering/calibratedWorkSpace.csv', 'w') as f:
            writer = csv.writer(f)
            for i in range(len(ids)):
               writer.writerow(p[i])

        with open('Realsense_Work/Projection_Rendering/arUCoCorners.csv', 'w') as f:
            writer = csv.writer(f)
            for i in range(4):
                writer.writerow(addCorners[i])

        np.save('Realsense_Work/Calibration_Procedure/type/calibration.npy', p)
    

