"""
PyViewer Module
"""

import sys
from PyQt5.Qt import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap

try:
    import PyViewer.utils as utl
except ImportError:
    import utils as utl

FOLDER = "C:/Users/mt/OneDrive - Istituto Nazionale di Fisica Nucleare/" \
    "Pictures/from Google/Takeout/Google Photos/Camper - Agosto 2020"

max_w, max_h = 1000, 1000


class MyImageViewerApp(QWidget):
    """ PyViewer Class """

    def __init__(self, items):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = max_w
        self.height = max_h
        self.setWindowTitle('Image Viewer')
        self.img_index = 0
        self.items = items
        self.init_indices()
        self.init_ui()

    def init_indices(self):
        """ init indices """
        self.img_index = 0 if len(self.items) > 0 else -1

    def next_index_image(self):
        """ increment index of images """
        self.img_index = utl.next_index(self.img_index, self.items)

    def prev_index_image(self):
        """ decrement index of images """
        self.img_index = utl.prev_index(self.img_index, self.items)

    def get_image(self):
        """ get current image """
        if self.img_index == -1:
            return None
        else:
            return self.items[self.img_index]

    def load_image(self, img):
        """ load image """
        self.setWindowTitle(img["name"])
        pixmap = QPixmap(img["path"])
        scale_factor = max_w/pixmap.width() \
            if max_w/pixmap.width() < max_h/pixmap.height() \
            else max_h/pixmap.height()
        width, height = int(
            pixmap.width()*scale_factor), int(pixmap.height()*scale_factor)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyImageViewerApp(utl.get_list_of_files_with_info(FOLDER)["image"])
    sys.exit(app.exec_())
