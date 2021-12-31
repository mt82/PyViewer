"""
map_viewer package
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

try:
    import PyViewer.utils as utl
except ImportError:
    import utils as utl

FOLDER="C:/Users/mt/OneDrive - Istituto Nazionale di Fisica Nucleare/" \
    "Pictures/from Google/Takeout/Google Photos/Camper - Agosto 2020"

max_w, max_h = 1000, 1000

class MyMapApp(QWidget):
    """
    Class to show map
    """
    def __init__(self, data):
        super().__init__()
        self.width = max_w
        self.height = max_h
        self.setWindowTitle('Map Viewer')
        # self.window_width, self.window_height = 1600, 1200
        # self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        web_view = QWebEngineView()
        web_view.setHtml(data.getvalue().decode())
        layout.addWidget(web_view)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    ex = MyMapApp(utl.build_map(utl.get_list_of_files_with_info(FOLDER)["image"]))
    sys.exit(app.exec_())
