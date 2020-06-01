import cv2 
import numpy as np 
import imutils
from PyQt5.QtWidgets import (QAction, QFileDialog, QApplication)
# from PyQt5.QtGui import QIcon
import sys
from pathlib import Path

class accion_video():
    def __init__(self,tvideo):
        self.tipovideo=tvideo

    def video(self):
        cap = cv2.VideoCapture(self.tipovideo) 
        if (cap.isOpened()== False):
            print("Error en cargar archivo") 
        while(cap.isOpened()): 
            ret, frame = cap.read() 
            if ret ==False:
                print('Error en cargar frame')
                break           
            else:
                frame = imutils.resize(frame, width=600)
                cv2.imshow('Circulo', frame) 
                if cv2.waitKey(25) & 0xFF == ord('q'): 
                    break
            
        cap.release() 
        cv2.destroyAllWindows() 