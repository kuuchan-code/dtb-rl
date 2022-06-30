#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as plt

THRESHOLD = 0.95
# 背景色 (bgr)
BACKGROUND_COLOR = np.array([251, 208, 49], dtype=np.uint8)
BACKGROUND_COLOR_LIGHT = BACKGROUND_COLOR + 4
BACKGROUND_COLOR_DARK = BACKGROUND_COLOR - 4
BLACK = np.zeros(3, dtype=np.uint8)
WHITE = BLACK + 255
WHITE_DARK = WHITE - 15


def bgr_extraction(image, bgr_lower, bgr_upper, inverse=False):
    """
    BGRで特定の色を抽出する関数
    """
    # cv2.bitwise_not()
    img_mask = cv2.inRange(image, bgr_lower, bgr_upper)  # BGRからマスクを作成
    if inverse:
        img_mask = cv2.bitwise_not(img_mask)
    result = cv2.bitwise_and(image, image, mask=img_mask)  # 元画像とマスクを合成
    # print(result)
    return result


def counter_shadow_extraction(image):
    """
    数値の影抽出
    もっと簡単にできなかったか...
    """
    img_mask = cv2.bitwise_not(cv2.inRange(
        image, BACKGROUND_COLOR_LIGHT, WHITE_DARK))
    result = cv2.bitwise_and(image, image, mask=img_mask)
    img_mask = cv2.bitwise_not(cv2.inRange(
        image, BACKGROUND_COLOR_DARK, WHITE)
    )
    result = cv2.bitwise_not(cv2.bitwise_and(result, result, mask=img_mask))
    img_mask = cv2.bitwise_not(cv2.inRange(result, BLACK, WHITE - 1))
    return cv2.bitwise_and(result, result, mask=img_mask)


img_bgr = cv2.imread("sonoda/num0_cloud.png")
# 動物の数の部分
img_bgr = img_bgr[260:330, 0:300, :]

fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot(3, 4, 1)
ax.imshow(img_bgr[:, :, ::-1])
ax.axis("off")

# ごにょごにょ
# img_bgr = bgr_extraction(
#     img_bgr, WHITE_DARK, BACKGROUND_COLOR_LIGHT, inverse=True)
# img_bgr = bgr_extraction(
#     img_bgr, BACKGROUND_COLOR_DARK, WHITE, inverse=True)
# img_bgr = cv2.bitwise_not(img_bgr)
# img_bgr = bgr_extraction(img_bgr, BLACK, WHITE - 1, inverse=True)
img_bgr = counter_shadow_extraction(img_bgr)

ax = fig.add_subplot(3, 4, 2)
ax.imshow(img_bgr[:, :, ::-1])
ax.axis("off")

img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

idx = 3

dict_digits = {}
for i in list(range(10)):
    template = cv2.imread(f"images/count{i}_shadow.png", 0)
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
