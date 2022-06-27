#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as plt

img_rgb = cv2.imread("samples/1.38.png")
img_rgb = img_rgb[65:129, 0:1080, :]
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

fig = plt.figure(figsize=(8, 5))
idx = 1
threshold = 0.8

dict_digits = {}
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
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv2.imwrite('res.png', img_rgb)
height = ""
for key in sorted(dict_digits.items()):
    if key[1] == "dot":
        height += "."
    else:
        height += str(key[1])
print(height)
plt.show()
