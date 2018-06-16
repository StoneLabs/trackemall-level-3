from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv2
import numpy as np
from darknet.pydarknet import Image
  
def doloop():
    global depth, rgb
    while True:
        # Get a fresh frame
        (depth,_), (rgb,_) = get_depth(), get_video()
        rgb = np.array(rgb)
        
        print(rgb)
        # Simple Downsample
        cv2.imshow('both', rgb)
        k = cv2.waitKey(1)
        
doloop()