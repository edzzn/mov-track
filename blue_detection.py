import cv2
import numpy as np
from matplotlib import pyplot as plt

from matplotlib.widgets import Slider

lower_r = 100
lower_g = 100
lower_b = 6

upper_r = 100
upper_g = 100
upper_b = 6

greenLower = (lower_r, lower_g, lower_b)
# greenLower = (29, 86, 6)
# greenUpper = (64, 255, 255)
greenUpper = (upper_r, upper_g, upper_b)

img = cv2.imread('rgb.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
blurred = cv2.GaussianBlur(img, (11, 11), 0)

hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# cv.namedWindow('Images')
# fig = plt.figure(1)
# plt.axis('off')

fig, ax_list = plt.subplots(1, 2)
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

ax_list = ax_list.ravel()

ax_list[0].set_title('Original Image')
ax_list[0].imshow(blurred)
ax_list[0].axis('off')

fig.subplots_adjust(bottom=0.2) 
plt.tight_layout()

# edges = cv2.Canny(img,minVal,maxVal)


mask = cv2.inRange(hsv, greenLower, greenUpper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)


ax_list[1].set_title('mask')
ax_list[1].imshow(mask)
ax_list[1].axis('off')





# Sliders
axSlider_lower_r = plt.axes([0.1, 0.1, 0.2, 0.03])
slder_lower_r = Slider(
              axSlider_lower_r,
              'lower_r',
              valmin=0,
              valmax=255,
              valinit=lower_r,
              valstep=10,
					    color='red'
              )

axSlider_upper_r = plt.axes([0.6, 0.1, 0.2, 0.03])
slder_upper_r = Slider(
              axSlider_upper_r,
              'upper_r',
              valmin=0,
              valmax=255,
              valinit=upper_r,
              valstep=10,
					    color='red'
              )

axSlider_lower_g = plt.axes([0.1, 0.06, 0.2, 0.03])
slder_lower_g = Slider(	ax=axSlider_lower_g,
					label='lower_g',
					valmin=0,
					valmax=255,
          valinit=lower_g,
					valfmt='%1.2f',
					valstep=10,
					closedmax=True,
					color='green',
        )

axSlider_upper_g = plt.axes([0.6, 0.06, 0.2, 0.03])
slder_upper_g = Slider(	ax=axSlider_upper_g,
					label='upper_g',
					valmin=0,
					valmax=255,
          valinit=upper_g,
					valfmt='%1.2f',
					valstep=10,
					closedmax=True,
					color='green',
        )

axSlider_lower_b = plt.axes([0.1, 0.01, 0.2, 0.03])
slder_lower_b = Slider(	ax=axSlider_lower_b,
					label='lower_b',
					valmin=0,
					valmax=255,
          valinit=lower_b,
					valfmt='%1.2f',
					valstep=10,
					closedmax=True,
					color='blue')

axSlider_upper_b = plt.axes([0.6, 0.01, 0.2, 0.03])
slder_upper_b = Slider(	ax=axSlider_upper_b,
					label='upper_b',
					valmin=0,
					valmax=255,
          valinit=upper_b,
					valfmt='%1.2f',
					valstep=10,
					closedmax=True,
					color='blue')



def update(val):
  lower_r = slder_lower_r.val
  lower_g = slder_lower_g.val
  lower_b = slder_lower_b.val
  upper_r = slder_upper_r.val
  upper_g = slder_upper_g.val
  upper_b = slder_upper_b.val
  # edges = cv2.Canny(img, minVal, maxVal)
  greenLower = (lower_r, lower_g, lower_b)
  greenUpper = (upper_r, upper_g, upper_b)
  mask = cv2.inRange(hsv, greenLower, greenUpper)
  mask = cv2.erode(mask, None, iterations=2)
  mask = cv2.dilate(mask, None, iterations=2)
  ax_list[1].imshow(mask)

slder_lower_r.on_changed(update)
slder_lower_g.on_changed(update)
slder_lower_b.on_changed(update)


slder_upper_r.on_changed(update)
slder_upper_g.on_changed(update)
slder_upper_b.on_changed(update)



plt.show()
