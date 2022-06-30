#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as plt

THRESHOLD = 0.99
# 背景色 (bgr)
BACKGROUND_COLOR = np.array([255, 208, 49])

# img_bgr = cv2.imread("samples/5.88.png")
img_bgr = cv2.imread("sonoda/num18.png")
img_bgr = img_bgr[260:330, 0:300, :]

fig = plt.figure(figsize=(8, 5))


def bgrExtraction(image, bgr_lower, bgr_upper):
    """
    BGRで特定の色を抽出する関数
    """
    img_mask = cv2.inRange(image, bgr_lower, bgr_upper)  # BGRからマスクを作成
    result = cv2.bitwise_and(image, image, mask=img_mask)  # 元画像とマスクを合成
    print(result)
    return result


# print(img_bgr)
ax = fig.add_subplot(3, 4, 1)
ax.imshow(img_bgr[:, :, ::-1])
img_bgr = bgrExtraction(img_bgr, BACKGROUND_COLOR, BACKGROUND_COLOR)
ax = fig.add_subplot(3, 4, 2)
ax.imshow(img_bgr[:, :, ::-1])

img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

idx = 3

dict_digits = {}
for i in list(range(10)):
    template = cv2.imread(f"images/count{i}.png", 0)
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
    height += str(key[1])

print(height)
plt.show()
