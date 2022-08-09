# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
##############################################################################

"""
Perform inference on a single image or all images with a certain extension
(e.g., .jpg) in a folder.

Modified to read image & generate IUV map via ROS topics
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
import argparse
import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
import glob
import logging
import os
import sys
import time

from caffe2.python import workspace

from detectron.core.config import assert_and_infer_cfg
from detectron.core.config import cfg
from detectron.core.config import merge_cfg_from_file
from detectron.utils.io import cache_url
from detectron.utils.logging import setup_logging
from detectron.utils.timer import Timer
import detectron.core.test_engine as infer_engine
import detectron.datasets.dummy_datasets as dummy_datasets
import detectron.utils.c2 as c2_utils
# ============= modified vis_one_image to return IUV =============
import detectron.utils.vis_mod as vis_utils

# publish IUV to ROS topic
import rospy
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

c2_utils.import_detectron_ops()

# OpenCL may be enabled by default in OpenCV3; disable it because it's not
# thread safe and causes unwanted GPU memory allocations.
# cv2.ocl.setUseOpenCL(False)


def parse_args():
  parser = argparse.ArgumentParser(description='End-to-end inference')
  parser.add_argument(
      '--cfg',
      dest='cfg',
      help='cfg model file (/path/to/model_config.yaml)',
      default=os.path.join(os.path.dirname(__file__), '../configs/DensePose_ResNet101_FPN_s1x-e2e.yaml'),
      type=str
  )
  parser.add_argument(
      '--wts',
      dest='weights',
      help='weights model file (/path/to/model_weights.pkl)',
      default=os.path.join(os.path.dirname(__file__), '../DensePoseData/DensePose_ResNet101_FPN_s1x-e2e.pkl'),
      type=str
  )
  parser.add_argument(
      '--output-dir',
      dest='output_dir',
      help='directory for visualization pdfs (default: /tmp/infer_simple)',
      default='/tmp/infer_simple',
      type=str
  )
  parser.add_argument(
      '--image-ext',
      dest='image_ext',
      help='image file name extension (default: png)',
      default='png',
      type=str
  )
  parser.add_argument(
      '--image',
      dest='image',
      help='input image',
      default=os.path.join(os.path.dirname(__file__), '../DensePoseData/image_buffer/incoming.png'),
      type=str
  )
  # if len(sys.argv) == 1:
  #   parser.print_help()
  #   sys.exit(1)
  return parser.parse_args()


image_input = None


def image_callback(msg):
  global image_input
  image_input = CvBridge().imgmsg_to_cv2(msg, desired_encoding="passthrough")


def main(args):
  logger = logging.getLogger(__name__)
  merge_cfg_from_file(args.cfg)
  cfg.NUM_GPUS = 1
  args.weights = cache_url(args.weights, cfg.DOWNLOAD_CACHE)
  assert_and_infer_cfg(cache_urls=False)
  model = infer_engine.initialize_model_from_cfg(args.weights)
  dummy_coco_dataset = dummy_datasets.get_coco_dataset()

  rospy.init_node('DensePosePublisher', anonymous=True)
  IUV_pub = rospy.Publisher('IUV', Image, queue_size=10)
  image_sub = rospy.Subscriber('DensePoseInput', Image, image_callback)
  repeatedRun = True
  readFromFile = False
  try:
    while not rospy.is_shutdown():
      if readFromFile:
        im = cv2.imread(args.image)
      else:
        if image_input is not None:
          im = image_input
        else:
          continue
      timers = defaultdict(Timer)
      t = time.time()
      with c2_utils.NamedCudaScope(0):
        cls_boxes, cls_segms, cls_keyps, cls_bodys = infer_engine.im_detect_all(
            model, im, None, timers=timers)
      logger.info('Inference time: {:.3f}s'.format(time.time() - t))
      for k, v in timers.items():
        logger.info(' | {}: {:.3f}s'.format(k, v.average_time))
      # ============= modified vis_one_image to return IUV =============
      IUV = \
          vis_utils.vis_one_image(
              im[:, :, ::-1],  # BGR -> RGB for visualization
              args.image,
              args.output_dir,
              cls_boxes,
              cls_segms,
              cls_keyps,
              cls_bodys,
              dataset=dummy_coco_dataset,
              box_alpha=0.3,
              show_class=True,
              thresh=0.7,     # 0.7
              kp_thresh=2
          )
      if IUV is not None:
        IUV_pub.publish(CvBridge().cv2_to_imgmsg(IUV, encoding="passthrough"))
      else:
        print("no target detected")
      if repeatedRun is False:
        break
  except KeyboardInterrupt:
    print("terminated by user")


if __name__ == '__main__':
  workspace.GlobalInit(['caffe2', '--caffe2_log_level=0'])
  setup_logging(__name__)
  args = parse_args()
  main(args)
