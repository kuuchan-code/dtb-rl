#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as plt

img_gray = cv2.imread("test.png", 0)
# img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
# img_bgr = img_bgr[65:129, 0:300]


fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
ax.imshow(img_gray, cmap="gray")
ax.axis("off")
plt.show()
