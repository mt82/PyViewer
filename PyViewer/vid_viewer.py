import sys
from types import prepare_class
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
        self.setWindowTitle('Video Viewer')
        self.vid_index = 0
        self.items = items
        self.init_indices()
        self.init_ui()

    def init_indices(self):
        """ init indices """
        self.vid_index = 0 if len(self.items) > 0 else -1

    def init_video(self, item):
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(item["path"])))

    def get_video(self):
        """ get current video """
        if self.vid_index == -1:
            return None
        else:
            return self.items[self.vid_index]
    
    def load_video(self,vid):
        self.setWindowTitle(vid["name"])
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(vid["path"])))

 
    def prev_index_video(self):
        """ decrement index of videos """
        self.vid_index = utl.prev_index(self.vid_index, self.items)

    def next_index_video(self):
        """ increment index of videos """
        self.vid_index = utl.next_index(self.vid_index, self.items)

    def init_ui(self):
        """ init UI """
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        self.setLayout(layout)
        self.media_player.setVideoOutput(self.video_widget)
        self.load_video(self.get_video())
        self.show()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.media_player.state() == QMediaPlayer.PlayingState:
                self.media_player.pause()
            else:
                self.media_player.play()

    def keyPressEvent(self, event):
        """ key pressed event """
        is_playing = (self.media_player.state() == QMediaPlayer.PlayingState)
        if event.key() == Qt.Key_Space:
            self.next_index_video()
            self.init_video(self.get_video())
            self.media_player.play() if is_playing else self.media_player.pause()
        elif event.key() == Qt.Key_Right:
            self.next_index_video()
            self.init_video(self.get_video())
            self.media_player.play() if is_playing else self.media_player.pause()
        elif event.key() == Qt.Key_Left:
            self.prev_index_video()
            self.init_video(self.get_video())
            self.media_player.play() if is_playing else self.media_player.pause()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyVideoViewerApp(utl.get_list_of_files_with_info(FOLDER)["video"])
    sys.exit(app.exec_())
