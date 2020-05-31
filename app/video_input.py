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
        self.detector = None

    def grab(self):
        with mss.mss() as sct:
            monitor = {'top': self.top, 'left': self.left,
                       'width': self.width, 'height': self.height}
            while(True):
                while(self.running):
                    debugFrames = []
                    if self.queue.qsize() < 10:
                        frame = np.array(sct.grab(monitor))
                        img = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                        if (self.detector):
                            img = self.detector.detect(
                                img, debugFrames=debugFrames)

                        self._addToQueue(img, debugFrames)

                        if(self.recording):
                            self._record(img)

                        if(self.should_take_screenshot):
                            self._take_screenshot(img)
                    else:
                        print(self.queue.qsize())

    def _addToQueue(self, image, debug):
        if (len(debug) == 0):
            self.queue.put((image, None))
        else:
            self.queue.put((image, *debug))

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

    def setDetector(self, detector):
        self.detector = detector
