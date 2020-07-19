import cv2
import numpy as np
from PIL import Image
from object_records import RegisteredObject


class DetectionBordes:
    def __init__(self, canny_th1=50, canny_th2=150, ksize_h=5, ksize_w=5, showTags=False, showCordenates=False):
        self.canny_th1 = canny_th1
        self.canny_th2 = canny_th2
        self.ksize_h = ksize_h
        self.ksize_w = ksize_w
        self.showTags = showTags
        self.showCordenates = showCordenates

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

        line_contours = self.getContornos(imgCanny, imgContorno)
        circle_contours = self.getCircles(imgBlur, imgContorno)
        validContours = line_contours + circle_contours

        object_records.add_all(validContours)

        for i, countour in enumerate(object_records.objects):
            countour.object_type = f"{countour.object_type} - {i}"
            self._draw_contour_name(
                imgContorno,
                countour
            )
            self._draw_contour(
                imgContorno,
                countour
            )

            self._draw_path(
                imgContorno,
                countour
            )

            self._draw_center(
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

    def getCircles(self, gray_image, imgContorno):
        valid_objects = []
        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1.2, 100)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            for (c_x, c_y, c_r) in circles:
                x = c_x - c_r
                y = c_y - c_r
                w = 2 * c_r
                h = 2 * c_r
                circle_object = RegisteredObject(x, y, w, h, 'Circulo')
                valid_objects.append(circle_object)
        return valid_objects

    def _draw_contour(self, image, object, color=(0, 255, 0), trickness=2):
        cv2.rectangle(
            image,
            (object.x, object.y),
            (object.x+object.w, object.y+object.h),
            color,
            trickness
        )

    def _draw_path(self, image, object, color=(255, 0, 255)):
        # print(f"Path: {object.path}")
        for point in object.path:
            cv2.circle(
                image,
                (point[0]+(object.w//2), point[1]+(object.h//2)),
                1,
                color,
                2
            )

    def _draw_center(self, image, object, color=(0, 0, 255)):
        cv2.circle(
            image,
            (object.x+(object.w//2), object.y+(object.h//2)),
            1,
            color,
            2
        )

    def _draw_contour_name(self, image, object, color=(0, 255, 0)):
        if (self.showTags):
            cv2.putText(
                image,
                object.object_type,
                (object.x+(object.w//2)-10, object.y+(object.h//2) - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                0.8,
                (0, 0, 0),
                4
            )
            cv2.putText(
                image,
                object.object_type,
                (object.x+(object.w//2)-10, object.y+(object.h//2) - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                0.8,
                color,
                2
            )

        if(self.showCordenates):
            # Draw coordanates
            cv2.putText(
                image,
                f"({str(object.x)},{str(object.y)})",
                (object.x+(object.w//2) + 7, object.y+(object.h//2) + 7),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 0, 0),
                2
            )
            cv2.putText(
                image,
                f"({str(object.x)},{str(object.y)})",
                (object.x+(object.w//2) + 7, object.y+(object.h//2) + 7),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                color,
                1
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
