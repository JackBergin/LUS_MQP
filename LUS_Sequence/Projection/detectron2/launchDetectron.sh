cd /home/medfuslab/Documents/GitHub/LUS_MQP/LUS_Sequence/Detectron2
python3 apply_net.py show configs/densepose_rcnn_R_50_FPN_s1x_legacy.yaml DensePoseData/DensePose_ResNet101_FPN_s1x-e2e.pkl DensePoseData/Detectron2Test.png dp_segm --output DensePoseData/densepose_segment.png
