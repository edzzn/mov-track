import mss
import numpy as np
import cv2


class VideoIn():
    def __init__(self, running, queue, top=0, left=0, width=400, height=400, hasTreadStarted=False, recording=False):
        self.running = running
        self.recording = recording
        self.queue = queue
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.hasTreadStarted = hasTreadStarted
        self.writer = None
        self.counter = 0
        self.img_counter = 0
        self.should_take_screenshot = False

    def grab(self):
        with mss.mss() as sct:
            monitor = {'top': self.top, 'left': self.left,
                       'width': self.width, 'height': self.height}
            while(True):
                while(self.running):
                    if self.queue.qsize() < 10:
                        frame = np.array(sct.grab(monitor))
                        self.queue.put(frame)
                        if(self.recording):
                            self._record(frame)

                        if(self.should_take_screenshot):
                            self._take_screenshot(frame)
                    else:
                        print(self.queue.qsize())

    def _record(self, image):
        self.img_counter += 1
        if(self.writer):
            self.writer.write(image[..., :3])

    def start_record(self):
        filename = f'records/record-{self.counter}.avi'
        codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        framerate = 30
        resolution = (self.width,  self.height)
        self.writer = cv2.VideoWriter(filename, codec, framerate, resolution)
        self.counter += 1

    def stop(self):
        if(self.writer):
            self.writer.release()

    def _take_screenshot(self, image):
        cv2.imwrite(
            f'records/screenshot-{self.img_counter}.jpg', image)
        self.img_counter += 1
        self.should_take_screenshot = False

    def take_screenshot(self):
        self.should_take_screenshot = True
