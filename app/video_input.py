import mss
import numpy as np


class VideoIn():
    def __init__(self, running, queue, top=0, left=0, width=400, height=400, hasTreadStarted=False):
        self.running = running
        self.queue = queue
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.hasTreadStarted = hasTreadStarted

    def grab(self):
        with mss.mss() as sct:
            monitor = {'top': self.top, 'left': self.left,
                       'width': self.width, 'height': self.height}
            while(True):
                while(self.running):
                    if self.queue.qsize() < 10:
                        frame = np.array(sct.grab(monitor))

                        self.queue.put(frame)
                    else:
                        print(self.queue.qsize())
