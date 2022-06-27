#!/usr/bin/env python3
import cv2
import argparse
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(
    description="トリミング")    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument("file_src", help="入力ファイル名")    # 必須の引数を追加
parser.add_argument("file_dst", help="出力ファイル名")    # 必須の引数を追加
# オプション引数（指定しなくても良い引数）を追加
parser.add_argument("--x0", type=int, default=0)
parser.add_argument("--x1", type=int, default=0x7fffffff)
parser.add_argument("--y0", type=int, default=0)
parser.add_argument("--y1", type=int, default=0x7fffffff)

args = parser.parse_args()    # 4. 引数を解析

print(args.file_src, args.file_dst, args.x0, args.x1, args.y0, args.y1)

# グレースケール読み込み
img_gray = cv2.imread(args.file_src, 0)

print(img_gray.shape)

x0 = args.x0
x1 = min(img_gray.shape[0], args.x1)
y0 = args.y0
y1 = min(img_gray.shape[1], args.y1)

# トリミング
img_gray = img_gray[x0: x1, y0: y1]

print(img_gray.shape)
cv2.imwrite(args.file_dst, img_gray)

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
ax.imshow(img_gray, cmap="gray", vmin=0, vmax=255)
ax.axis("off")
plt.show()
