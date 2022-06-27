#!/usr/bin/env python3
import itertools
import gym
import numpy as np
from appium import webdriver
from time import sleep
import cv2


THRESHOLD = 0.99

caps = {}
caps["platformName"] = "android"
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:newCommandTimeout"] = 3600
caps["appium:connectHardwareKeyboard"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)


def calc_height(img_gray):
    dict_digits = {}
    for i in list(range(10))+["dot"]:
        template = cv2.imread("digits/"+str(i)+".png", 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= THRESHOLD)
        for y in loc[1]:
            dict_digits[y] = i
    height = ""
    for key in sorted(dict_digits.items()):
        if key[1] == "dot":
            height += "."
        else:
            height += str(key[1])
    return float(height)


class AnimalTower(gym.Env):
    def __init__(self):
        a = np.linspace(0, 1080, 64)
        b = np.linspace(0, 7, 8)
        self.ACTION_MAP = np.array([v for v in itertools.product(a, b)])
        self.action_space = gym.spaces.Discrete(512)       # エージェントが取りうる行動空間を定義
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(256, 144))  # エージェントが受け取りうる観測空間を定義
        self.reward_range = [-1, 1]       # 報酬の範囲[最小値と最大値]を定義

    def reset(self):
        # リスタートボタンをタップ
        pass
        driver.save_screenshot('test.png')
        I = cv2.imread("test.png")
        I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
        I = cv2.resize(I, dsize=(256, 144))
        observation = I
        # スタート後の画像を返す？
        return observation

    def step(self, action_index):
        action = self.ACTION_MAP[action_index]
        # actionのようにタップする
        pass
        driver.save_screenshot('test.png')
        img_bgr = cv2.imread("test.png")
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        img_gray_resized = cv2.resize(img_gray, dsize=(256, 144))
        observation = img_gray_resized
        if calc_height(img_gray) > prev_height:
            reward = 1
            done = False
        # 落としたらreward -1
        elif 落としたら:
            reward = -1
            done = True
        # つめたらreward 0
        else:
            reward = 0
            done = False

        return observation, reward, done, {}

    def render(self):
        # プレイ画面を返す？
        pass
