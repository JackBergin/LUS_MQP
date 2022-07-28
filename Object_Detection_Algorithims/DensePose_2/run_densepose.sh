#!/bin/zsh

~/anaconda2/bin/python2 tools/infer_simple.py \
    --cfg configs/DensePose_ResNet101_FPN_s1x-e2e.yaml \
    --output-dir DensePoseData/infer_out/ \
    --image-ext png \
    --wts DensePoseData/DensePose_ResNet101_FPN_s1x-e2e.pkl \
    ~/DensePose/DensePoseData/image_buffer       
