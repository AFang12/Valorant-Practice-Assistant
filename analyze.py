import time
import cProfile

import torch
import onnxruntime as ort
import numpy as np
import cv2
from ultralytics.utils.checks import check_requirements

from YOLOv8 import YOLOv8

def analyze(video_path, key_log_path):        
    # ONNX模型
    model_path = r"weights\n_test.onnx"
   
    conf_thres = .5
    iou_thres = .5
    
    # Check the requirements and select the appropriate backend (CPU or GPU)
    check_requirements("onnxruntime-gpu" if torch.cuda.is_available() else "onnxruntime")
    
    detection = YOLOv8(model_path, video_path, conf_thres, iou_thres)
    res = detection.main()
    print("目标检测完成，分析中")
    print(time.time())
    # for box, score, class_id, t in res['res']:
        # t代表视频开始后的第t帧
        # left, top, width, height = box[0], box[1], box[2], box[3]
        # print(time.time())
        # print(item)
    for item in res['res']:
        print(type(item))

if __name__ == "__main__":
    print('1',time.time())
    analyze(r"E:\botDet\video\test.mp4", r"E:\\botDet\\video\\key_log.txt")
    # cProfile.run('analyze(r"E:\\botDet\\video\\test.mp4", r"E:\\botDet\\video\\key_log.txt")')
    print(time.time())