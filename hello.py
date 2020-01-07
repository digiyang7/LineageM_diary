
# 使用hook來打包
import imagehash

# adb.py
from PIL import ImageGrab
import win32gui, win32ui, win32con, win32api
import subprocess
from threading import Thread


# lineageM.py
from PIL import Image
import cv2
import numpy as np
import os,time

class Hello:
    def __init__(self):
        pass
    def start(self):
        while 1:
            print("hello")
            time.sleep(10)

if __name__ == '__main__':
    h = Hello()
    h.start()