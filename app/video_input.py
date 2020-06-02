import mss
import numpy as np
import cv2
import time

from object_records import ObjectsRecord


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
        # Keep track of registered Objects
        self.objects_record = ObjectsRecord()
        self.source = ''
    
    def _processingFrame(self, frame):
            debugFrames = []
            img = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
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
        self.source = new_source

    def grab(self):
        while True:
            print(f"Showing: {self.source}")
            # if (self.source=='screen'):
            #     with mss.mss() as sct:
            #         monitor = {'top': self.top, 'left': self.left,
            #                 'width': self.width, 'height': self.height}
            #         # while(True):
            #         while(self.running):
            #             if self.queue.qsize() < 10:
            #                 frame = np.array(sct.grab(monitor))
            #                 self._processingFrame(frame)
                        
            # # elif (self.source='webcam'):
            # else:
            #     cap = cv2.VideoCapture(self.source) 
            #     if (not cap.isOpened()):
            #         print("Error en cargar archivo") 
            #     while(cap.isOpened()): 
            #         while(self.running):
            #             if self.queue.qsize() < 10:
            #                 ret, frame = cap.read() 
            #                 self._processingFrame(frame)

        # elif (self.source='cellcam'):
        #     cap = cv2.VideoCapture(1) 
        #     if (cap.isOpened()== False):
        #         print("Error en cargar archivo") 
        #     while(cap.isOpened()): 
        #         while(self.running):
        #             debugFrames = []
        #             if self.queue.qsize() < 10:
        #                 ret, frame = cap.read()
        #                 self._processingFrame(frame) 
        # else:
        #     cap = cv2.VideoCapture(path) 
        #     if (cap.isOpened()== False):
        #         print("Error en cargar archivo") 
        #     while(cap.isOpened()): 
        #         while(self.running):
        #             debugFrames = []
        #             if self.queue.qsize() < 10:
        #                 ret, frame = cap.read() 
        #                 self._processingFrame(frame)

    # def grabwebcam(self):
    #     cap = cv2.VideoCapture(0) 
    #     if (cap.isOpened()== False):
    #         print("Error en cargar archivo") 
    #     while(cap.isOpened()): 
    #         while(self.running):
    #             debugFrames = []
    #             if self.queue.qsize() < 10:
    #                 ret, frame = cap.read() 
                    
    #                 #  self.widht = ...
    #                 img = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    #                 if (self.detector):
    #                     img = self.detector.detect(
    #                         img,
    #                         debugFrames=debugFrames,
    #                         object_records=self.objects_record
    #                     )
    #                 self._addToQueue(img, debugFrames)
    #                 if(self.recording):
    #                     self._record(img)

    #                 if(self.should_take_screenshot):
    #                     self._take_screenshot(img)
    # def grabcellcam(self):
    #     cap = cv2.VideoCapture(1) 
    #     if (cap.isOpened()== False):
    #         print("Error en cargar archivo") 
    #     while(cap.isOpened()): 
    #         while(self.running):
    #             debugFrames = []
    #             if self.queue.qsize() < 10:
    #                 ret, frame = cap.read() 
    #                 img = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    #                 if (self.detector):
    #                     img = self.detector.detect(
    #                         img,
    #                         debugFrames=debugFrames,
    #                         object_records=self.objects_record
    #                     )
    #                 self._addToQueue(img, debugFrames)
    #                 if(self.recording):
    #                     self._record(img)

    #                 if(self.should_take_screenshot):
    #                     self._take_screenshot(img)
    # def grabplayvideo(self,path):
        # cap = cv2.VideoCapture(path) 
        # if (cap.isOpened()== False):
        #     print("Error en cargar archivo") 
        # while(cap.isOpened()): 
        #     while(self.running):
        #         debugFrames = []
        #         if self.queue.qsize() < 10:
        #             ret, frame = cap.read() 
        #             img = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        #             if (self.detector):
        #                 img = self.detector.detect(
        #                     img,
        #                     debugFrames=debugFrames,
        #                     object_records=self.objects_record
        #                 )
        #             self._addToQueue(img, debugFrames)
        #             if(self.recording):
        #                 self._record(img)

        #             if(self.should_take_screenshot):
        #                 self._take_screenshot(img)

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

