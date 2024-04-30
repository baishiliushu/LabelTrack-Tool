from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI.utils import *
import sys
import os
import cv2


class fileWorker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, canvas):
        super().__init__()
        self.path = None
        self.canvas = canvas
    
    def load_path(self, path):
        self.path = path
    
    def run(self):
        self.load_frames()

    def load_frames(self):
        if os.path.isdir(self.path):
            self.canvas.imgFrames = []
            files = get_image_list(self.path)
            self.canvas.src_img_names = files
            numFrames = len(files)
            for i, file in enumerate(files):
                frame = cv2.imread(file)
                self.canvas.imgFrames.append(frame)
                if i % 30 == 0:
                    self.sinOut.emit("已加载图片帧 {} / {}".format(i, numFrames))
        else:
            self.canvas.imgFrames = []
            if "mp4" not in self.path:
                return
            self.canvas.videoCapture = cv2.VideoCapture(self.path)

            numFrames = self.canvas.videoCapture.get(7)
            self.canvas.src_img_names = ["{}_{}".format(self.path, i) for i in range(0, numFrames)]
            rval = self.canvas.videoCapture.isOpened()
            i = 0
            while rval: 
                rval, frame = self.canvas.videoCapture.read()  
                if rval:
                    self.canvas.imgFrames.append(frame)
                if i % 30 == 0:
                    self.sinOut.emit("已加载图片帧 {} / {}".format(i, numFrames))
                i += 1
        if len(self.canvas.src_img_names) != numFrames:
            print("ERR,exit, files_name {} != numFrames {}".format(len(self.canvas.src_img_names), numFrames))
        self.sinOut.emit("图片帧已加载完成：{}".format(len(self.canvas.src_img_names)))