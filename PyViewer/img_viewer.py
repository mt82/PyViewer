from PyQt5 import QtCore
try:
    import PyViewer.utils as utl
except:
    import utils as utl
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt

folder="C:/Users/mt/OneDrive - Istituto Nazionale di Fisica Nucleare/Pictures/from Google/Takeout/Google Photos/Camper - Agosto 2020"

max_w, max_h = 1000, 1000

def nextIndex(this_index, collection):
    if len(collection) == 0:
        this_index = -1
    elif this_index == len(collection) - 1:
        this_index = 0
    else:
        this_index += 1
    return this_index

def prevIndex(this_index, collection):
    if len(collection) == 0:
        this_index = -1
    elif this_index == 0:
        this_index = len(collection) - 1
    else:
        this_index -= 1
    return this_index

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = max_w
        self.height = max_h
        self.items = utl.getListOfFilesWithInfo(folder)
        self.initIndices()
        self.initUI()
    
    def initIndices(self):
        self.img_index = 0 if len(self.items["image"]) > 0 else -1
        self.vid_index = 0 if len(self.items["video"]) > 0 else -1
    
    def nextIndexImage(self):
        self.img_index = nextIndex(self.img_index, self.items["image"])
    
    def nextIndexVideo(self):
        self.vid_index = nextIndex(self.vid_index, self.items["video"])
    
    def prevIndexImage(self):
        self.img_index = prevIndex(self.img_index, self.items["image"])
    
    def prevIndexVideo(self):
        self.vid_index = prevIndex(self.vid_index, self.items["video"])
    
    def getImage(self):
        if self.img_index == -1:
            return None
        else:
            return self.items["image"][self.img_index]
    
    def getVideo(self):
        if self.vid_index == -1:
            return None
        else:
            return self.items["video"][self.vid_index]
    
    def loadImage(self, img):
        self.setWindowTitle(img["name"])
        pixmap = QPixmap(img["path"])
        scale_factor = max_w/pixmap.width() if max_w/pixmap.width() < max_h/pixmap.height() else  max_h/pixmap.height()
        width, height = int(pixmap.width()*scale_factor), int(pixmap.height()*scale_factor)
        pixmap = pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.resize(width, height)
        self.label.resize(width, height)
    
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label = QLabel(self)
        self.loadImage(self.getImage())
        self.show()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.nextIndexImage()
            self.loadImage(self.getImage())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.nextIndexImage()
            self.loadImage(self.getImage())
        elif event.key() == Qt.Key_Right:
            self.nextIndexImage()
            self.loadImage(self.getImage())
        elif event.key() == Qt.Key_Left:
            self.prevIndexImage()
            self.loadImage(self.getImage())
   
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,
                                                    "QFileDialog.getOpenFileName()", 
                                                    "",
                                                    "All Files (*);;Python Files (*.py)", 
                                                    options=options)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())