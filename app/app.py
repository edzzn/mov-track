from ui_widgets import OwnImageWidget
from video_input import VideoIn
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import cv2
import numpy as np
import threading
import time
import queue as Queue
from bordes_detection import DetectionBordes

capture_thread = None
form_class = uic.loadUiType("tracker.ui")[0]

q = Queue.Queue()
video_in = VideoIn(False, q, width=1500, height=800)
canny_detector = DetectionBordes()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('tracker.ui', self)  # Load the .ui file

        self.startButton.clicked.connect(self.start_clicked)
        self.recordButton.clicked.connect(self.record_clicked)
        self.tagsButton.clicked.connect(self.tags_clicked)
        self.cordenatesButton.clicked.connect(self.cordenates_clicked)
        self.screenshotButton.clicked.connect(self.screenshot_clicked)
        self.trackButton.clicked.connect(self.track_clicked)

        # Sliders
        self.cannySlider_th1.valueChanged.connect(self.cannySlider_th1_changed)
        self.cannySlider_th2.valueChanged.connect(self.cannySlider_th2_changed)
        self.ksizeSlider_w.valueChanged.connect(self.ksizeSlider_w_changed)
        self.ksizeSlider_h.valueChanged.connect(self.ksizeSlider_h_changed)

        # Default slider values
        self.cannySlider_th1.setValue(canny_detector.canny_th1)
        self.cannySlider_th2.setValue(canny_detector.canny_th2)
        self.ksizeSlider_h.setValue(canny_detector.ksize_h)
        self.ksizeSlider_w.setValue(canny_detector.ksize_w)

        self.ImgWidget = OwnImageWidget(self.ImgWidget)
        self.window_width = self.ImgWidget.frameSize().width()
        self.window_height = self.ImgWidget.frameSize().height()

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

    def track_clicked(self):
        global video_in
        global canny_detector

        if (not self.trackButton.isChecked()):
            video_in.setDetector(None)
            self.trackButton.setChecked(False)
        else:
            self.trackButton.setChecked(True)
            video_in.setDetector(canny_detector)

    def tags_clicked(self):
        global canny_detector
        if (not self.tagsButton.isChecked()):
            self.tagsButton.setChecked(False)
            canny_detector.showTags = False
        else:
            self.tagsButton.setChecked(True)
            canny_detector.showTags = True

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

            img_height, img_width, _img_colors = img.shape
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

    def cannySlider_th1_changed(self):
        global canny_detector

        sliderValue = self.cannySlider_th1.value()
        self.canny_th1.setText(str(sliderValue))

        canny_detector.setCanny(
            canny_th2=self.cannySlider_th2.value()
        )

    def cannySlider_th2_changed(self):
        sliderValue = self.cannySlider_th2.value()
        self.canny_th2.setText(str(sliderValue))

        canny_detector.setCanny(
            canny_th1=self.cannySlider_th1.value()
        )

    def ksizeSlider_h_changed(self):
        sliderValue = self.ksizeSlider_h.value()
        sliderValue -= (1 - sliderValue % 2)

        self.ksize_h.setText(str(sliderValue))
        canny_detector.setKsize(
            ksize_h=sliderValue
        )

    def ksizeSlider_w_changed(self):
        sliderValue = self.ksizeSlider_w.value()
        sliderValue -= (1 - sliderValue % 2)

        self.ksize_w.setText(str(sliderValue))
        canny_detector.setKsize(
            ksize_w=sliderValue
        )


capture_thread = threading.Thread(
    target=video_in.grab)

# Iniciar instancia de QT
app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.setWindowTitle('Deteción de Objetos')
window.show()
app.exec_()
