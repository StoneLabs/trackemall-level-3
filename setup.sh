#!/usr/bin/env bash
download_weights() {
    echo "=> Downloading weights (140BnF)"
    mkdir weights
    wget https://pjreddie.com/media/files/yolov3.weights -O weights/yolov3-608-140Bn.weights -q --show-progress
    ln weights/yolov3-608-140Bn.weights weights/yolov3.weights
}
download_cfg() {
    echo "=> Downloading configs (140BnF)"
    mkdir cfg
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/coco.data -O cfg/coco.data -q --show-progress
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg -O cfg/yolov3.cfg -q --show-progress
}

if [ -d "./weights/" ]; then
    rm -rf ./weights/ 
fi
download_weights

if [ -d "./cfg/" ]; then
    rm -rf ./cfg/
fi
download_cfg

echo "=> Building darknet\(TM\)"
cd darknet
python3 setup.py build_ext --inplace
cd ..
