#!/usr/bin/env python3
import cv2
import argparse
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(
    description="トリミング")    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument("file", help="ファイル名")    # 必須の引数を追加
# オプション引数（指定しなくても良い引数）を追加
parser.add_argument("--x0", type=int, default=None)
parser.add_argument("--x1", type=int, default=None)
parser.add_argument("--y0", type=int, default=None)
parser.add_argument("--y1", type=int, default=None)

args = parser.parse_args()    # 4. 引数を解析

print(args.file, args.x0, args.x1, args.y0, args.y1)

# グレースケール読み込み
img_gray = cv2.imread("test.png", 0)

print(img_gray.shape)

# トリミング
img_gray = img_gray[1000:, :500]

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
ax.imshow(img_gray, cmap="gray")
ax.axis("off")
plt.show()
