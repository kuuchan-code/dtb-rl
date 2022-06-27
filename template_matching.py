#!/usr/bin/env python3
import cv2
import numpy as np

img_rgb = cv2.imread("samples/2.52.png")
img_rgb = img_rgb[65:129, 0:1080, :]
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

dict_digits = {}
for i in list(range(10))+["dot"]:
    template = cv2.imread("digits/"+str(i)+".png",0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.99
    loc = np.where(res >= threshold)
    if len(loc[1]) != 0:
        for y in loc[1]:
            dict_digits[y] = i
    for pt in zip(*loc[::-1]):  
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv2.imwrite('res.png',img_rgb)
height = ""
for key in sorted(dict_digits.items()):
    if key[1] == "dot":
        height += "."
    else:
        height += str(key[1])
print(height)