#!/bin/bash

echo 'running test_sys_utils...'
python3 -m unittest utils/test_sys_utils.py 

echo 'running test_video_utils...'
python3 -m unittest utils/test_video_utils.py 
