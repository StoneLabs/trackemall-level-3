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

    while True: # Dont judge please
        time_start = time.time()
        print("Grabbing data... [ PREPARING ]", end='', flush=True)
        cmd = ['wget', "192.168.12.1:2438/getNext", "-O", "/tmp/next_frame.id", "wb+"]
        prc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input="")
        with open('/tmp/next_frame.id', 'r') as content_file:
            _id = content_file.read()

        print("\rGrabbing data... [  LOADING  ] \t#" + str(_id), end='', flush=True)
        cmd = ['wget', "192.168.12.1:2438/getFrame?id=" + str(_id), "-O", "/tmp/next_frame.dat", "wb+"]
        prc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input="")

        print("\rGrabbing data... [ IMPORTING ] \t#" + str(_id), end='', flush=True)
        with open("/tmp/next_frame.dat", "rb") as handle:
            frame = pickle.load(handle)

        print("\rGrabbing data... [ DETECTING ] \t#" + str(_id), end='', flush=True)
        dark_frame = Image(frame)
        results = net.detect(dark_frame)

        print("\rGrabbing data... [ ANSWERING ] \t#" + str(_id), end='', flush=True)
        with open("/tmp/next_frame.det", "wb+") as handle:
            time_up_start = time.time()

            pickle.dump({"results": results, "frame": frame}, handle) # im sorry
            # DUMP TO STRING?

            # SEND TO SQL?
            cmd = ['curl', '-i', '-X', 'POST', '-H', "Content-Type: multipart/form-data", '-F', "file=@/tmp/next_frame.det", "http://192.168.12.1:2438/setDetection?id=" + str(_id)]
            prc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input="")

            cmd = ['rm', "/tmp/next_frame.det", "wb+"]
            prc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input="")

        print("\rGrabbing data... [   DONE!   ] \t#" + str(_id), end='', flush=True)
        print(" | Upload (s): " + str(round(time.time() - time_up_start, 2)), end='', flush=True)
        print(" | Total (s): " + str(round(time.time() - time_start, 2)), end='', flush=True)
        print(" | FPS: " + str(round(1 / (time.time() - time_start), 2)), flush=True)
        # Send back results
