#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as plt

img_bgr = cv2.imread("samples/2.19.png")
img_bgr = img_bgr[60:140, 0:300, :]
dict_digits = {}
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
threshold = 0.8

fig = plt.figure(figsize=(8, 5))
idx = 1

for i in list(range(10))+["dot"]:
    ax = fig.add_subplot(3, 4, idx)
    idx += 1
    template = cv2.imread(f"digits/{i}.png", 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    ax.imshow(res)
    ax.axis("off")
    loc = np.where(res >= threshold)
    print(len(loc))
    for j in loc:
        print(j)
    if len(loc[1]) != 0:
        dict_digits[loc[1].min()] = i
    for pt in zip(*loc[::-1]):
        # print(pt)
        cv2.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv2.imwrite("res.png", img_bgr)
print(sorted(dict_digits.items()))
plt.show()
