from PyQt5 import QtCore
from utils import getListOfFilesWithInfo
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt

folder="C:/Users/mt/OneDrive - Istituto Nazionale di Fisica Nucleare/Pictures/from Google/Takeout/Google Photos/Camper - Agosto 2020"

max_w, max_h = 1000, 1000

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 100
        self.top = 100
        self.width = max_w
        self.height = max_h
        self.items = getListOfFilesWithInfo(folder)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        label = QLabel(self)
        pixmap = QPixmap(self.items["image"][0]["path"])
        scale_factor = max_w/pixmap.width() if max_w/pixmap.width() < max_h/pixmap.height() else  max_h/pixmap.height()
        width, height = int(pixmap.width()*scale_factor), int(pixmap.height()*scale_factor)
        pixmap = pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        self.resize(width, height)
        
        self.show()
		
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space or event.key() == Qt.Key_Right:
            self.test_method()

    def test_method(self):
        print('Space key pressed')
    
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