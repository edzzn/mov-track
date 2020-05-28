from ui_widgets import OwnImageWidget
from video_input import VideoIn
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import cv2
import numpy as np
import threading
import time
import queue as Queue

capture_thread = None
form_class = uic.loadUiType("tracker.ui")[0]

q = Queue.Queue()
video_in = VideoIn(False, q, width=1920, height=800)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi('tracker.ui', self)  # Load the .ui file

        self.startButton.clicked.connect(self.start_clicked)
        self.recordButton.clicked.connect(self.record_clicked)
        self.tagsButton.clicked.connect(self.tags_clicked)
        self.cordenatesButton.clicked.connect(self.cordenates_clicked)
        self.screenshotButton.clicked.connect(self.screenshot_clicked)

        self.ImgWidget = OwnImageWidget(self.ImgWidget)
        self.window_width = self.ImgWidget.frameSize().width()
        self.window_height = self.ImgWidget.frameSize().height()

        p = self.ImgWidget.palette()
        p.setColor(self.ImgWidget.backgroundRole(), QtGui.QColor('red'))
        self.ImgWidget.setPalette(p)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def start_clicked(self):
        global video_in

        if (not video_in.hasTreadStarted):
            capture_thread.start()
            video_in.hasTreadStarted = True

        if (video_in.running):
            video_in.running = False
            self.startButton.setText('Iniciar')
            self.startButton.setChecked(False)
        else:
            video_in.running = True
            self.startButton.setText('Pausar')
            self.startButton.setChecked(True)

    def record_clicked(self):
        global video_in
        if (not self.recordButton.isChecked()):
            self.recordButton.setText('Grabar')
            self.recordButton.setChecked(False)
            video_in.recording = False
            video_in.stop()

        else:
            self.recordButton.setText('Detener')
            self.recordButton.setChecked(True)
            video_in.recording = True

            video_in.start_record()

    def tags_clicked(self):
        if (not self.tagsButton.isChecked()):
            self.tagsButton.setChecked(False)
        else:
            self.tagsButton.setChecked(True)

    def cordenates_clicked(self):
        if (not self.cordenatesButton.isChecked()):
            self.cordenatesButton.setChecked(False)
        else:
            self.cordenatesButton.setChecked(True)

    def screenshot_clicked(self):
        global video_in
        video_in.take_screenshot()

    def update_frame(self):
        if not q.empty():
            global video_in
            window_width = 1000
            window_height = 800

            frame = q.get()
            img = frame

            img_height, img_width, img_colors = img.shape
            scale_w = float(window_width) / float(img_width)
            scale_h = float(window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale,
                             interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bytes_per_line = bpc * width
            image = QtGui.QImage(img.data, width, height,
                                 bytes_per_line, QtGui.QImage.Format_RGB888)
            self.ImgWidget.setImage(image)

    def closeEvent(self, event):
        global video_in
        video_in.running = False
        video_in.stop()


capture_thread = threading.Thread(
    target=video_in.grab)

# Iniciar instancia de QT
app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.setWindowTitle('Deteción de Objetos')
window.show()
app.exec_()
