#import os
import time
import numpy as np
from darknet.pydarknet import Detector, Image
from numpy import asarray
from PIL import Image as PImage
import subprocess
import pickle


if __name__ == "__main__":

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))

    while True:
        print("Grabbing data... ", end='', flush=True)
        cmd = ['wget', "127.0.0.1:2438/getNext", "-O", "/tmp/next_frame.dat", "wb+"]
        prc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input="")

        print("\rGrabbing data... [ IMPORTING ]", end='', flush=True)
        with open("/tmp/next_frame.dat", "rb") as handle:
            frame = pickle.load(handle)

        print("\rGrabbing data... [ DETECTING ]", end='', flush=True)
        dark_frame = Image(frame)
        results = net.detect(dark_frame)

        print("\rGrabbing data... [ ANSWERING ]", end='', flush=True)
        print("\rGrabbing data... [   DONE!   ]", flush=True)
        # Send back results