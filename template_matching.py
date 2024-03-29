#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as plt

THRESHOLD = 0.99

img_bgr = cv2.imread("samples/5.88.png")
img_bgr = img_bgr[65:129, 0:300, :]
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

fig = plt.figure(figsize=(8, 5))
idx = 1

dict_digits = {}
for i in list(range(10))+["dot"]:
    template = cv2.imread(f"digits/{i}.png", 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    ax = fig.add_subplot(3, 4, idx)
    ax.imshow(res)
    ax.axis("off")
    idx += 1
    loc = np.where(res >= THRESHOLD)
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
plt.show()
