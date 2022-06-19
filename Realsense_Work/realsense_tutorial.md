# instructions on working with RealSense D435i



## 1. Using [pyrealsense2](https://pypi.org/project/pyrealsense2/?msclkid=87d0b7aaaefe11ecacac772cccae5192) (recommanded)
### dependencies
python >= 3.6

### installation
``` bash
pip3 install pyrealsense2
```

### official python examples
https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples

### utility class
| file name                 | description                             |
| ------------------------- | --------------------------------------- |
| ```GetRealSenseData.py``` | class for streaming data from realsense |
| ```GetSurfaceNormal.py``` | required by ```GetRealSenseData.py```   |

## 2. Using [RealSense ROS package](https://github.com/IntelRealSense/realsense-ros)

### install [librealsense](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md)
register the server's public key:
``` shell
sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
```

add repository (tested on Ubuntu18.04)
``` shell
sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo bionic main" -u
```

install libraires
``` shell
sudo apt-get install librealsense2-dkms
sudo apt-get install librealsense2-utils
sudo apt-get install librealsense2-dev
sudo apt-get install librealsense2-dbg
```

### clone and build ROS package
under [catkin workspace name]/src
```shell
git clone https://github.com/IntelRealSense/realsense-ros.git
cd ..
catkin_make -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release
catkin_make install
source ./devel/setup.zsh
```

### usage
read pointcloud in ROS
``` shell
roslaunch realsense2_camera rs_camera.launch filters:=pointcloud
```
check pointcloud data
``` shell
rostopic echo /camera/depth/color/points
```

## 3. Using [MATLAB](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/matlab) (Windows10 only)


## 4. Other approaches
refer to [librealsense](https://github.com/IntelRealSense/librealsense) for more info


