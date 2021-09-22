"""
PyViewer Module
"""

import sys
from PyQt5.Qt import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap

try:
    import PyViewer.utils as utl
except ImportError:
    import utils as utl

FOLDER="C:/Users/mt/OneDrive - Istituto Nazionale di Fisica Nucleare/" \
    "Pictures/from Google/Takeout/Google Photos/Camper - Agosto 2020"

max_w, max_h = 1000, 1000

def next_index(this_index, collection):
    """ get next index """
    if len(collection) == 0:
        this_index = -1
    elif this_index == len(collection) - 1:
        this_index = 0
    else:
        this_index += 1
    return this_index

def prev_index(this_index, collection):
    """ get previous index """
    if len(collection) == 0:
        this_index = -1
    elif this_index == 0:
        this_index = len(collection) - 1
    else:
        this_index -= 1
    return this_index

class App(QWidget):
    """ PyViewer Class """

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = max_w
        self.height = max_h
        self.img_index = 0
        self.vid_index = 0
        self.filename = ""
        self.items = utl.get_list_of_files_with_info(FOLDER)
        self.init_indices()
        self.init_ui()

    def init_indices(self):
        """ init indices """
        self.img_index = 0 if len(self.items["image"]) > 0 else -1
        self.vid_index = 0 if len(self.items["video"]) > 0 else -1

    def next_index_image(self):
        """ increment index of images """
        self.img_index = next_index(self.img_index, self.items["image"])

    def next_index_video(self):
        """ increment index of videos """
        self.vid_index = next_index(self.vid_index, self.items["video"])

    def prev_index_image(self):
        """ decrement index of images """
        self.img_index = prev_index(self.img_index, self.items["image"])

    def prev_index_video(self):
        """ decrement index of videos """
        self.vid_index = prev_index(self.vid_index, self.items["video"])

    def get_image(self):
        """ get current image """
        if self.img_index == -1:
            return None
        else:
            return self.items["image"][self.img_index]

    def get_video(self):
        """ get current video """
        if self.vid_index == -1:
            return None
        else:
            return self.items["video"][self.vid_index]

    def load_image(self, img):
        """ load image """
        self.setWindowTitle(img["name"])
        pixmap = QPixmap(img["path"])
        scale_factor = max_w/pixmap.width() \
            if max_w/pixmap.width() < max_h/pixmap.height() \
            else  max_h/pixmap.height()
        width, height = int(pixmap.width()*scale_factor), int(pixmap.height()*scale_factor)
        pixmap = pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.resize(width, height)
        self.label.resize(width, height)

    def init_ui(self):
        """ init UI """
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label = QLabel(self)
        self.load_image(self.get_image())
        self.show()

    def mousePressEvent(self, event):
        """ mouse click event """
        if event.button() == Qt.LeftButton:
            self.next_index_image()
            self.load_image(self.get_image())

    def keyPressEvent(self, event):
        """ key pressed event """
        if event.key() == Qt.Key_Space:
            self.next_index_image()
            self.load_image(self.get_image())
        elif event.key() == Qt.Key_Right:
            self.next_index_image()
            self.load_image(self.get_image())
        elif event.key() == Qt.Key_Left:
            self.prev_index_image()
            self.load_image(self.get_image())

    def openFileNameDialog(self):
        """ open filename dialog """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.filename = QFileDialog.getOpenFileName(self, \
            "QFileDialog.getOpenFileName()", \
            "", \
            "All Files (*);;Python Files (*.py)", \
            options=options)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
