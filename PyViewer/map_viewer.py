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

class MyMapApp(QWidget):
    """
    Class to show map
    """
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('Map Viewer')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        web_view = QWebEngineView()
        web_view.setHtml(data.getvalue().decode())
        layout.addWidget(web_view)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    ITEMS = None

    NARGS = len(sys.argv)
    if NARGS == 1:
        ITEMS = utl.get_list_of_files_with_info(FOLDER)
    elif NARGS == 2:
        ITEMS = utl.get_list_of_files_with_info(sys.argv[1])

    else:
        print("  -- Too many arguments --")
        sys.exit(1)

    myApp = MyMapApp(utl.build_map(ITEMS["image"]))
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
