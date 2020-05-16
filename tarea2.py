from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


greenLower = (100, 150, 130)
greenUpper = (200, 255, 255)
pts = deque(maxlen=32)
# lower_blue = np.array([110,50,50])
# upper_blue = np.array([130,255,255])

# frame = cv2.imread('figurasColores2.png')
frame= cv2.imread('case.jpeg')

frame = imutils.resize(frame, width=600)
blurred = cv2.GaussianBlur(frame, (11, 11), 0)

hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, greenLower, greenUpper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)


cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
  cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print(cnts)



# center = None
# # only proceed if at least one contour was found
if len(cnts) > 0:
#   # find the largest contour in the mask, then use
#   # it to compute the minimum enclosing circle and
#   # centroid
  c = max(cnts, key=cv2.contourArea)
  ((x, y), radius) = cv2.minEnclosingCircle(c)
  M = cv2.moments(c)
  center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#   # only proceed if the radius meets a minimum size
  # if radius > 10:
#     # draw the circle and centroid on the frame,
#     # then update the list of tracked points
#     cv2.circle(frame, (int(x), int(y)), int(radius),
#       (0, 255, 255), 2)
  cv2.circle(frame, center, 5, (0, 255, 0), -1)
#     pts.appendleft(center)

# cv2.imshow('frame',frame)
# cv2.imshow('blurred',blurred)
# cv2.imshow('hsv',hsv)
# cv2.imshow('mask',mask)

# cv2.waitKey(0)


for c in cnts:
  epsilon = 0.01*cv2.arcLength(c,True)
  approx = cv2.approxPolyDP(c,epsilon,True)
  # print(len(approx))
  x,y,w,h = cv2.boundingRect(approx)

  # if len(approx)==3:
  #   cv2.putText(frame,'Triangulo', (x,y-5),1,1.5,(0,255,0),2)
  #   print(f"Numero de lados: {len(approx)}\t Figura: Triangulo")

  # if len(approx)==4:
  #   aspect_ratio = float(w)/h
  #   # print('aspect_ratio= ', aspect_ratio)
  #   if aspect_ratio == 1:
  #     cv2.putText(frame,'Cuadrado', (x,y-5),1,1.5,(0,255,0),2)
  #     print(f"Numero de lados: {len(approx)}\t Figura: Cuadrado")
  #   else:
  #     cv2.putText(frame,'Rectangulo', (x,y-5),1,1.5,(0,255,0),2)
  #     print(f"Numero de lados: {len(approx)}\t Figura: Rectangulo")

  # if len(approx)==5:
  #   cv2.putText(frame,'Pentagono', (x,y-5),1,1.5,(0,255,0),2)

  #   print(f"Numero de lados: {len(approx)}\t Figura: Pentagono")

  # if len(approx)==6:
  #   cv2.putText(frame,'Hexagono', (x,y-5),1,1.5,(0,255,0),2)
  #   print(f"Numero de lados: {len(approx)}\t Figura: Hexagono")

  if len(approx)>4 :
    # cv2.putText(frame,'Poligono', (x,y-5),1,1.5,(0,255,0),2))
    cv2.drawContours(frame, [approx], 0, (0,255,0),2)
    print(f"Numero de lados: {len(approx)}\t Figura: Poligono")

  # if len(approx)>10:
  #   cv2.putText(frame,'Circulo', (x,y-5),1,1.5,(0,255,0),2)
  #   print(f"Numero de lados: {len(approx)}\t Figura: Circulo")

  
  cv2.imshow('frame',frame)
  cv2.imshow('mask',mask)
  cv2.waitKey(0)