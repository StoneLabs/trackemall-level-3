#import os
import time
import numpy as np
import cv2
from freenect import sync_get_depth as get_depth, sync_get_video as get_video
from darknet.pydarknet import Detector, Image
from numpy import asarray
from PIL import Image as PImage

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

if __name__ == "__main__":

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))

    while True:
        # Receive frame matricies

        start_time = time.time()

        dark_frame = Image(frame)
        results = net.detect(dark_frame)

        # Send back results