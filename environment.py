from appium import webdriver
import itertools
import gym
import numpy as np
from appium import webdriver
from time import sleep
import cv2
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

THRESHOLD = 0.99


def calc_height(img_gray):
    """
    パターンマッチングで高さ計算
    """
    img_gray_height = img_gray[65:129, :]
    dict_digits = {}
    for i in list(range(10))+["dot"]:
        template = cv2.imread(f"digits/{i}.png", 0)
        res = cv2.matchTemplate(
            img_gray_height, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= THRESHOLD)
        for y in loc[1]:
            dict_digits[y] = i
    height = ""
    for key in sorted(dict_digits.items()):
        if key[1] == "dot":
            height += "."
        else:
            height += str(key[1])
    if height:
        height = float(height)
    else:
        height = None
    return height


def check_guruguru(img_gray):
    """
    パターンマッチングでぐるぐるを探す
    """
    img_gray_guruguru = img_gray
    template = cv2.imread("digits/record.png", 0)
    res = cv2.matchTemplate(
        img_gray_guruguru, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= THRESHOLD)
    if len(loc[1]) > 0:
        print("ぐるぐるしてる")
    else:
        print("ぐるぐるしてない")
    return len(loc[1]) > 0


class AnimalTower(gym.Env):
    def __init__(self):
        print("初期化")
        a = np.linspace(0, 7, 8)
        b = np.linspace(0, 1079, 64)
        self.ACTION_MAP = np.array([v for v in itertools.product(a, b)])
        self.action_space = gym.spaces.Discrete(512)       # エージェントが取りうる行動空間を定義
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=(144, 256))  # エージェントが受け取りうる観測空間を定義
        self.reward_range = [-1, 1]       # 報酬の範囲[最小値と最大値]を定義
        self.prev_height = -1  # 初期値変更
        caps = {}
        caps["platformName"] = "android"
        caps["appium:ensureWebviewsHavePages"] = True
        caps["appium:nativeWebScreenshot"] = True
        caps["appium:newCommandTimeout"] = 3600
        caps["appium:connectHardwareKeyboard"] = True
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.operations = ActionChains(self.driver)
        self.operations.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))

    def reset(self):
        print("リセット!!")
        # 高さもリセット
        self.prev_height = -1
        # リスタートボタンをタップ
        self._tap(200, 1755)
        sleep(3)
        img_gray = cv2.imread("test.png", 0)
        img_gray_resized = cv2.resize(img_gray, dsize=(256, 144))
        observation = img_gray_resized
        # スタート後の画像を返す
        return observation

    def step(self, action_index):
        for i in range(10):
            self.operations.perform()
            self.driver.save_screenshot("test.png")
            img_gray = cv2.imread("test.png", 0)
            height = calc_height(img_gray)
            # 終わり
            if height is None:
                if check_guruguru(img_gray):
                    print("done")
                    return cv2.resize(img_gray, dsize=(256, 144)), -1, True, {}
            # 高さ更新
            elif height > self.prev_height:
                break
            sleep(1)
            print(f"待機中{i}")
        # actionのようにタップする
        action = self.ACTION_MAP[action_index]
        # 回数分タップ
        for _ in range(int(action[0])):
            self._tap(500, 1800)
            # print("回転")
        self._tap(action[1], 800)

        self.operations.perform()
        self.driver.save_screenshot("test.png")
        img_gray = cv2.imread("test.png", 0)
        height = calc_height(img_gray)
        observation = cv2.resize(img_gray, dsize=(256, 144))
        print(height)
        if height and height > self.prev_height:
            reward = 1
            done = False
        elif height is None and check_guruguru(img_gray):
            reward = -1
            print("done")
            done = True
        else:
            reward = 0
            done = False
        self.prev_height = height

        return observation, reward, done, {}

    def render(self):
        # プレイ画面を返す？
        pass

    def _tap(self, x, y):
        """
        タップ
        """
        self.operations.w3c_actions.pointer_action.move_to_location(x, y)
        self.operations.w3c_actions.pointer_action.pointer_down()
        self.operations.w3c_actions.pointer_action.pause(0.1)
        self.operations.w3c_actions.pointer_action.release()
        self.operations.perform()
        sleep(0.1)
