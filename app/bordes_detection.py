import cv2
import numpy as np


class DetectionBordes:
    def __init__(self, canny_th1=50, canny_th2=150, ksize_h=5, ksize_w=5, showTags=False):
        self.canny_th1 = canny_th1
        self.canny_th2 = canny_th2
        self.ksize_h = ksize_h
        self.ksize_w = ksize_w
        self.showTags = showTags

    def setCanny(self, canny_th1=None, canny_th2=None):
        if (canny_th1):
            self.canny_th1 = canny_th1
        if (canny_th2):
            self.canny_th2 = canny_th2

    def setKsize(self, ksize_h=None, ksize_w=None):
        if (ksize_h):
            self.ksize_h = ksize_h
        if (ksize_w):
            self.ksize_w = ksize_w

    def detect(self, img):
        imgContorno = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (self.ksize_h, self.ksize_w), 0)

        imgCanny = cv2.Canny(imgBlur, self.canny_th1, self.canny_th2)
        self.getContornos(imgCanny, imgContorno)

        # print(f"org: {img.shape}\t imgBlur: {imgBlur.shape}")
        return imgContorno

    def getContornos(self, imagen, imgContorno):
        ret, thresh = cv2.threshold(imagen, 127, 255, 0)
        _, contorno, jerarquia = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contorno:
            area = cv2.contourArea(cnt)
            if area > 450:
                cv2.drawContours(imgContorno, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
                objCor = len(approx)
                x, y, w, h = cv2.boundingRect(approx)
                if objCor == 3:
                    objectType = "Triangulo"
                elif objCor == 4:
                    aspRatio = w/float(h)
                    if aspRatio > 0.98 and aspRatio < 1.03:
                        objectType = "Cuadrado"
                    else:
                        objectType = "Rectangulo"
                elif objCor == 5:
                    objectType = "Pentagono"
                elif objCor > 5:
                    objectType = "Circulo"
                else:
                    objectType = "None"
                cv2.rectangle(imgContorno, (x, y), (x+w, y+h), (0, 255, 0), 2)

                if (self.showTags):
                    # Mostrando el texto dos veces para tener margen
                    cv2.putText(imgContorno, objectType,
                                (x+(w//2)-10, y+(h//2) -
                                 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                (0, 0, 0), 4)
                    cv2.putText(imgContorno, objectType,
                                (x+(w//2)-10, y+(h//2) -
                                 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                (0, 255, 0), 2)
