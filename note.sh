echo Starting infinite loop in T-3
sleep 3
while true; do LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/darknet/ python3.6 note.py; done