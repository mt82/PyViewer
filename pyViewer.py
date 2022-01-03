
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

try:
    import PyViewer.utils as utl
    from PyViewer.img_viewer import *
    from PyViewer.map_viewer import *
except ImportError:
    import utils as utl

FOLDER = "C:/Users/mt/OneDrive - Istituto Nazionale di Fisica Nucleare/" \
    "Pictures/from Google/Takeout/Google Photos/Camper - Agosto 2020"


def openFileNameDialog():
    """ open filename dialog """
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    return QFileDialog.getExistingDirectory(None,
                                            "QFileDialog.getOpenFileName()",
                                            "",
                                            options=options)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    directory = openFileNameDialog()
    items = utl.get_list_of_files_with_info(directory)
    mp = utl.build_map(items["image"])
    myViewwer = MyImageViewerApp(items)
    myMap = MyMapViewerApp(mp)
    sys.exit(app.exec_())
