#import os
import time
import cv2
from darknet.pydarknet import Detector, Image
from numpy import asarray
from PIL import Image as PImage

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

pg.setConfigOptions(antialias=True)
application = QtGui.QApplication([])

window = pg.GraphicsWindow()
window.resize(1000,600)
window.setWindowTitle("Quality Software.to")
container = pg.ImageItem()
containerplot = window.addPlot()
containerplot.addItem(container)

if __name__ == "__main__":

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))

    success = False
    while (not success):
        print("Enter webcam id (0=default): ", end='')
        id=input()

        cap = cv2.VideoCapture(int(id))
        if(cap.isOpened()):
            print("Device opened successfully")
            success = True
        else:
            print("Couldn't open device")

    while True:
        r, frame = cap.read()
        if r:
            start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(frame)
            print("Calculating results...", end='', flush=True)
            results = net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            print(" [" + str(end_time-start_time) + "]")

            for cat, score, bounds in results:
                x, y, w, h = bounds
                cv2.rectangle(frame, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
                cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

            #cv2.imshow("preview", frame)
            container.setImage(asarray(PImage.fromarray(frame).rotate(-90)))

        k = cv2.waitKey(1)
        if k == 0xFF & ord("q"):
            break