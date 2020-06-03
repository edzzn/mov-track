import mss
import numpy as np
import cv2
import time
import datetime

from object_records import ObjectsRecord


class VideoIn():
    def __init__(self, running, queue, top=0, left=0, width=640, height=480, hasTreadStarted=False, recording=False):
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
        # Keep track of registered Objects
        self.objects_record = ObjectsRecord()
        self.source = ''
        self.video_cap = None

    def _processingFrame(self, frame):
        if (isinstance(frame, np.ndarray)):
            debugFrames = []
            img = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            img = self._reshape_image(img)
            if (self.detector):
                img = self.detector.detect(
                    img,
                    debugFrames=debugFrames,
                    object_records=self.objects_record
                )
            self._addToQueue(img, debugFrames)
            if(self.recording):
                self._record(img)
            if(self.should_take_screenshot):
                self._take_screenshot(img)

    def set_source(self, new_source):
        print(f"set_source(self, new_source): {new_source}")
        # Close video capture
        self.source = new_source
        if(self.video_cap):
            self.video_cap.release()

    def grab(self):
        while True:
            if (self.source == 'screen'):
                with mss.mss() as sct:
                    monitor = {'top': self.top, 'left': self.left,
                               'width': self.width, 'height': self.height}
                    while(self.running):
                        if self.queue.qsize() < 10:
                            frame = np.array(sct.grab(monitor))
                            self._processingFrame(frame)

            # elif (self.source='webcam'):
            else:
                self.video_cap = cv2.VideoCapture(self.source)
                if (not self.video_cap.isOpened()):
                    print("Error en cargar archivo")
                frame_counter = 0
                self.video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                while(self.video_cap.isOpened()):
                    while(self.running):
                        if self.queue.qsize() < 10:
                            ret, frame = self.video_cap.read()
                            frame_counter += 1
                            self._processingFrame(frame)

                        # Loop if source is a file
                        isStreamingFile = self.source != 0 and self.source != 1
                        if (isStreamingFile):
                            if frame_counter == self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT):
                                frame_counter = 0  # Or whatever as long as it is the same as next line
                                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def _addToQueue(self, image, debug):
        if (len(debug) == 0):
            self.queue.put((image, None))
        else:
            self.queue.put((image, *debug))

    def _reshape_image(self, image):
        window_width = self.width
        window_height = self.height

        canvas = np.ones((window_height, window_width, 3), np.uint8)*0

        img_height, img_width, _img_colors = image.shape
        scale_w = float(window_width) / float(img_width)
        scale_h = float(window_height) / float(img_height)
        scale = min([scale_w, scale_h])

        if scale == 0:
            scale = 1

        scaled_image = cv2.resize(image, None, fx=scale, fy=scale,
                                  interpolation=cv2.INTER_CUBIC)

        img_scaled_height, img_scaled_width, _img_scaled_colors = scaled_image.shape

        y_offset = (window_height - img_scaled_height) // 2
        x_offset = (window_width - img_scaled_width) // 2

        canvas[y_offset:y_offset+scaled_image.shape[0],
               x_offset:x_offset+scaled_image.shape[1]] = scaled_image

        return canvas

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

    def stop_record(self):
        if(self.writer):
            self.writer.release()

    def stop(self):
        if(self.writer):
            self.writer.release()

        if(self.video_cap):
            self.video_cap.release()

    def _take_screenshot(self, image):
        cv2.imwrite(
            f'records/screenshot-{self.img_counter}.jpg', image)
        self.img_counter += 1
        self.should_take_screenshot = False

    def take_screenshot(self):
        self.should_take_screenshot = True

    def setDetector(self, detector):
        self.detector = detector
