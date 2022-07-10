# Realsense Test
## Purpose
This library works with the direct controls of the Realsense camera in a python wrapper form. This allows easy access and integration within the code for the body detection and segmentation.
The following image is of the Realsense Camera D435 Web camera we are using:
![Screen Shot 2022-07-10 at 8 24 19 AM](https://user-images.githubusercontent.com/81708456/178144807-4db52d93-44b5-4e4f-bac5-ae69697a43f5.png)

The specs on this camera are as follows:
![Screen Shot 2022-07-10 at 8 25 04 AM](https://user-images.githubusercontent.com/81708456/178144823-bb3c96af-18a5-4006-9a32-f06bd7f1d27f.png)

The projector and camera system as a whole is mounted on top of a projector with the realsense being the top most component. Transforms to go from 2D pixel coordinants to 3D world coordinates are under way as a means to crop the depth component of the point cloud.
