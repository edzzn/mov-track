import cv2
import numpy as np
from PIL import Image
from video_input import RegisteredObject


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

    def detect(self, img, debugFrames=[], object_records=None):
        imgContorno = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (self.ksize_h, self.ksize_w), 0)

        imgCanny = cv2.Canny(imgBlur, self.canny_th1, self.canny_th2)

        validContours = self.getContornos(imgCanny, imgContorno)

        for countour in validContours:
            self._draw_contour_name(
                imgContorno,
                countour
            )
            self._draw_contour(
                imgContorno,
                countour
            )

        debugFrames.append(
            cv2.cvtColor(imgBlur, cv2.COLOR_GRAY2RGB)
        )

        debugFrames.append(
            cv2.cvtColor(imgCanny, cv2.COLOR_GRAY2RGB)
        )

        return imgContorno

    def _draw_contour(self, image, object):
        cv2.rectangle(
            image,
            (object.x, object.y),
            (object.x+object.w, object.y+object.h),
            (0, 255, 0),
            2
        )

    def _draw_contour_name(self, image, object):
        if (self.showTags):
            cv2.putText(
                image,
                object.object_type,
                (object.x+(object.w//2)-10, object.y+(object.h//2) - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                0.7,
                (0, 0, 0),
                4
            )
            cv2.putText(
                image,
                object.object_type,
                (object.x+(object.w//2)-10, object.y+(object.h//2) - 10),
                cv2.FONT_HERSHEY_COMPLEX, 0.7,
                (0, 255, 0),
                2
            )

    def getContornos(self, img, imgContorno):
        valid_Contours = []

        _ret, thresh = cv2.threshold(img, 127, 255, 0)
        _, contour, _jerarquia = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contour:
            area = cv2.contourArea(cnt)
            object_type = ''
            if area > 450:
                cv2.drawContours(imgContorno, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
                objCor = len(approx)
                x, y, w, h = cv2.boundingRect(approx)
                if objCor == 3:
                    object_type = "Triangulo"
                elif objCor == 4:
                    aspRatio = w/float(h)
                    if aspRatio > 0.98 and aspRatio < 1.03:
                        object_type = "Cuadrado"
                    else:
                        object_type = "Rectangulo"

                if objCor < 5 and object_type:
                    valid_Contour = RegisteredObject(x, y, w, h, object_type)
                    valid_Contours.append(valid_Contour)

        return valid_Contours
