#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as plt

img_bgr = cv2.imread("samples/1.11_2.png")
img_bgr = img_bgr[65:129, 0:1080, :]
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

fig = plt.figure(figsize=(8, 5))
idx = 1
THRESHOLD = 0.99
min_dist = 20

dict_digits = {}
for i in list(range(10))+["dot"]:
    ax = fig.add_subplot(3, 4, idx)
    idx += 1
    template = cv2.imread(f"digits/{i}.png", 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= THRESHOLD)
    print(loc[1])
    for y in loc[1]:
        dict_digits[y] = i
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
cv2.imwrite('res.png', img_bgr)
height = ""
for key in sorted(dict_digits.items()):
    if key[1] == "dot":
        height += "."
    else:
        height += str(key[1])
print(height)
# plt.show()
