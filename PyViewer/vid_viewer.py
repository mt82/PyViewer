import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QFileDialog, QStyle, QVBoxLayout, QWidget

try:
    import PyViewer.utils as utl
except ImportError:
    import utils as utl

FOLDER = "C:/Users/mt/OneDrive - Istituto Nazionale di Fisica Nucleare/" \
    "Pictures/from Google/Takeout/Google Photos/Camper - Agosto 2020"

max_w, max_h = 1000, 1000

class MyVideoViewerApp(QWidget):

    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.left = 100
        self.top = 100
        self.width = max_w
        self.height = max_h
        self.items = items
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)

        self.setLayout(layout)

        self.media_player.setVideoOutput(self.video_widget)

        self.init_video(items[0])
        self.init_ui()

    def init_video(self, item):
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(item["path"])))

    def init_ui(self):
        """ init UI """
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.label = QLabel(self)
        #self.load_image(self.get_image())
        self.show()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.media_player.state() == QMediaPlayer.PlayingState:
                self.media_player.pause()
            else:
                self.media_player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyVideoViewerApp(utl.get_list_of_files_with_info(FOLDER)["video"])
    sys.exit(app.exec_())
