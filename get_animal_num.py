#!/usr/bin/env python3
import cv2
import numpy as np

THRESHOLD = 0.97
# 背景色 (bgr)
BACKGROUND_COLOR = np.array([251, 208, 49], dtype=np.uint8)
BACKGROUND_COLOR_LIGHT = BACKGROUND_COLOR + 4
BACKGROUND_COLOR_DARK = BACKGROUND_COLOR - 5
BLACK = np.zeros(3, dtype=np.uint8)
WHITE = BLACK + 255
WHITE_DARK = WHITE - 15


def counter_shadow_extraction(image: np.ndarray) -> np.ndarray:
    """
    数値の影抽出
    もっと簡単にできなかったか...
    """
    img_mask = cv2.inRange(
        image, BACKGROUND_COLOR_DARK, WHITE)
    cv2.imwrite("ttest.png", img_mask)
    return img_mask


def get_animal_num(img_bgr: np.ndarray) -> int:
    """
    動物の数を取得
    引数にはカラー画像を与える!!
    """
    img_trim = img_bgr[264:328, :]
    img_shadow = counter_shadow_extraction(img_trim)
    dict_digits = {}
    for i in list(range(10)):
        template = cv2.imread(f"images/count{i}_shadow.png", 0)
        res = cv2.matchTemplate(
            img_shadow, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= THRESHOLD)
        # print(loc, i)
        for y in loc[1]:
            dict_digits[y] = i
    animal_num = ""
    for key in sorted(dict_digits.items()):
        animal_num += str(key[1])
    if not animal_num:
        animal_num = 0
    return int(animal_num)


if __name__ == "__main__":
    # 試したい画像を入れてみる
    img_bgr = cv2.imread("sonoda/num2_cloud.png")
    n = get_animal_num(img_bgr)
    print(n)
