from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import cv2
import numpy as np
import threading
import time
# from PyQt5.QtGui import QImage
try:
    import Queue
except ImportError:
    # Python 3
    import queue as Queue
import mss

running = False
capture_thread = None
form_class = uic.loadUiType("tracker.ui")[0]

q = Queue.Queue()


def grab(queue, width, height):
    global running
    with mss.mss() as sct:

        monitor = {'top': 220, 'left': 55, 'width': width, 'height': height}

        while(running):
            frame = np.array(sct.grab(monitor))

            if queue.qsize() < 10:
                queue.put(frame)
            else:
                print(queue.qsize())


class OwnImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None
        self.setImage(QtGui.QImage("ball2.png"))

    def setImage(self, image):
        # print(image)

        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi('tracker.ui', self)  # Load the .ui file

        self.startButton.clicked.connect(self.start_clicked)

        self.window_width = self.ImgWidget.frameSize().width()
        self.window_height = self.ImgWidget.frameSize().height()
        self.ImgWidget = OwnImageWidget(self.ImgWidget)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def start_clicked(self):
        global running
        running = True
        print('clicked')
        # capture_thread.start()
        self.startButton.setEnabled(False)
        self.startButton.setText('Starting...')

    def start_clicked(self):
        global running
        running = True
        capture_thread.start()
        self.startButton.setEnabled(False)
        self.startButton.setText('Starting...')

    def update_frame(self):
        if not q.empty():
            # print('processing queue')
            self.startButton.setText('Camera is live')
            frame = q.get()
            # img = frame["img"]
            img = frame

            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale,
                             interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QtGui.QImage(img.data, width, height,
                                 bpl, QtGui.QImage.Format_RGB888)
            self.ImgWidget.setImage(image)

    def closeEvent(self, event):
        global running
        running = False


capture_thread = threading.Thread(target=grab, args=(q, 800, 400))

# Create an instance of QtWidgets.QApplication
app = QtWidgets.QApplication(sys.argv)
window = Ui()  # Create an instance of our class
window.setWindowTitle('Test')
window.show()
app.exec_()  # Start the application
