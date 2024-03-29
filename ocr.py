#!/usr/bin/env python3
from PIL import Image
import pytesseract
import cv2
import numpy as np


# 画像の読み込み + グレースケール化
img = cv2.imread('./tpl_match.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

template = cv2.imread('./tpl_match_tpl.png')
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# 処理対象画像に対して、テンプレート画像との類似度を算出する
res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# 類似度の高い部分を検出する
threshold = 0.8
loc = np.where(res >= threshold)

# テンプレートマッチング画像の高さ、幅を取得する
h, w = template_gray.shape

# 検出した部分に赤枠をつける
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

# 画像の保存
cv2.imwrite('./tpl_match_after.png', img)


I = Image.open('test.png')
# I = I.convert("L").point(lambda x: 255 if x < 255 else 0, mode="1")
# I = I.crop((0,50,500,400))
I = I.crop((0, 50, 500, 300))
# I = ResizeImage(I)
I.save("test-cropped.png")
print(pytesseract.image_to_string(I, config="digits"))
print(pytesseract.image_to_string(I, lang="jpn", config="digits"))
