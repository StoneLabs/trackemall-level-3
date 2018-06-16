#!/usr/bin/env bash

ask() {
    # https://djm.me/ask
    local prompt default reply

    while true; do

        if [ "${2:-}" = "Y" ]; then
            prompt="Y/n"
            default=Y
        elif [ "${2:-}" = "N" ]; then
            prompt="y/N"
            default=N
        else
            prompt="y/n"
            default=
        fi

        # Ask the question (not using "read -p" as it uses stderr not stdout)
        echo -n "$1 [$prompt] "

        # Read the answer (use /dev/tty in case stdin is redirected from somewhere else)
        read reply </dev/tty

        # Default?
        if [ -z "$reply" ]; then
            reply=$default
        fi

        # Check if the reply is valid
        case "$reply" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac

    done
}

download_weights() {
    echo "=> Downloading weights (140BnF)"
    mkdir weights
    wget https://pjreddie.com/media/files/yolov3.weights -O weights/yolov3-608-140Bn.weights -q --show-progress
    ln weights/yolov3-608-140Bn.weights weights/yolov3.weights -s
}
download_cfg() {
    echo "=> Downloading configs (140BnF)"
    mkdir cfg
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/coco.data -O cfg/coco.data -q --show-progress
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg -O cfg/yolov3.data -q --show-progress
}

if [ -d "./weights/" ]; then
    if ask "++ Folder ./weights/ found! Delete it?" Y; then
        rm -rf ./weights/
        download_weights
    fi
else
    download_weights
fi

echo
if [ -d "./cfg/" ]; then
    if ask "++ Folder ./cfg/ found! Delete it?" Y; then
        rm -rf ./cfg/
        download_cfg
    fi
else
    download_cfg
fi

echo
if ask "++ Would you like to build darknet?" Y; then
    echo "=> Building darknet\(TM\)"
    cd darknet
    python3 setup.py build_ext --inplace
    cd ..
fi