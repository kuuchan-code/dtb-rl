from appium import webdriver
import itertools
import gym
import numpy as np
from time import sleep
import cv2
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import InvalidElementStateException

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
    img_gray_guruguru = img_gray[1600:, :]
    template = cv2.imread("images/guruguru.png", 0)
    res = cv2.matchTemplate(
        img_gray_guruguru, template, cv2.TM_CCOEFF_NORMED)
    # 判定をゆるくする
    loc = np.where(res >= 0.9)
    b = len(loc[1]) > 0
    return b


def check_record(img_gray):
    """
    パターンマッチングで record を探す
    """
    template = cv2.imread("digits/record.png", 0)
    res = cv2.matchTemplate(
        img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= THRESHOLD)
    b = len(loc[1]) > 0
    if b:
        print("ぐるぐるしてる")
    else:
        print("ぐるぐるしてない")
        b = check_guruguru(img_gray)
        if b:
            print("と思ったらぐるぐるしてる")
    return b


class AnimalTower(gym.Env):
    def __init__(self):
        print("初期化")
        a = np.linspace(0, 7, 8)
        b = np.linspace(0, 1079, 64)
        self.ACTION_MAP = np.array([v for v in itertools.product(a, b)])
        self.action_space = gym.spaces.Discrete(512)       # エージェントが取りうる行動空間を定義
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=(540, 960))  # エージェントが受け取りうる観測空間を定義
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
        observation = cv2.resize(img_gray, (960, 540))
        # スタート後の画像を返す
        return observation

    def step(self, action_index):
        """
        1ステップ
        """
        # actionのようにタップする
        action = self.ACTION_MAP[action_index]
        # 回数分タップ
        for _ in range(int(action[0])):
            self._tap(500, 1800)
            # print("回転")
        self._tap(action[1], 800)

        sleep(1)

        # デフォルトは0
        reward = 0

        # 報酬を計算
        for i in range(10):
            self.operations.perform()
            self.driver.save_screenshot("test.png")
            img_gray = cv2.imread("test.png", 0)
            observation = cv2.resize(img_gray, (960, 540))
            height = calc_height(img_gray)
            print(height, self.prev_height)
            if height is None:
                # 落ちた
                if check_record(img_gray):
                    print("done")
                    return observation, -1, True, {}
            # 高さ更新
            elif height != self.prev_height:
                if height > self.prev_height:
                    reward = 1
                self.prev_height = height
                break
            sleep(1)
            print(f"更新待機中{i}")
        # 続行
        return observation, reward, False, {}

    def render(self):
        # プレイ画面を返す？
        pass

    def _tap(self, x, y):
        """
        タップ
        """
        while True:
            try:
                self.operations.w3c_actions.pointer_action.move_to_location(
                    x, y)
                self.operations.w3c_actions.pointer_action.pointer_down()
                self.operations.w3c_actions.pointer_action.pause(0.1)
                self.operations.w3c_actions.pointer_action.release()
                self.operations.perform()
                break
            except InvalidElementStateException:
                print("エラー?")
