import os.path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time

class loadWorker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, canvas):
        super().__init__()
        self.labelPath = ""
        self.canvas = canvas

    def run(self):
        self.load_label()
    
    def load_path(self, labelPath):
        self.labelPath = labelPath

    def load_label(self):
        if not os.path.exists(self.labelPath):
            #self.sinOut.emit("[ERR]{} NOT exists.".format(self.labelPath))
            return
        with open(self.labelPath, "r") as f:
            count = len(open(self.labelPath,'rU').readlines())
            for i, line in enumerate(f.readlines(), 1):
                # line = line.strip('\n').split(',')
                line = line.replace("|", ",")
                line = line.replace(";", ",")
                lines = line.strip('\n').split(',')
                for ll in lines:
                    if ll == "":
                        print("[DEBUG]No.{}->{}:{}".format(i, line.strip('\n'), lines))
                        lines.remove(ll)
                if len(lines) < 7:
                    print("[continue]No.{}->{}:{}".format(i, line.strip('\n'), lines))
                    continue
                # print("[DEBUG]No.{}->{}:{}".format(i, line.strip('\n'), lines))
                tlwh = [int(lines[2]), int(lines[3]), int(lines[4]), int(lines[5])]
                self.canvas.update_shape(int(lines[1]), int(lines[0]), int(lines[7]), tlwh, float(lines[6]), 'L')
                if i % 10 == 0:
                    self.sinOut.emit("标注框已加载 {} / {}".format(i, count))
        self.sinOut.emit("标注文件已加载完成")
