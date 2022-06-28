#!/usr/bin/env python3
# 面倒なのでtrainも兼ねる
import os
from stable_baselines3 import PPO, A2C
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
from selenium.common.exceptions import InvalidElementStateException, WebDriverException

THRESHOLD = 0.99
WAITTIME_AFTER_DROP = 8
WAITTIME_AFTER_RESET = 3
POLLONG_INTERVAL = 1
WAITTIME_AFTER_ROTATION = 0.5
_WAITTIME_AFTER_ROTATION = 0.007
TAP_TIME = 0.01
RESET_BUTTON_COORDINATES = 200, 1755
ROTATE_BUTTON_COORDINATES = 500, 1800
NUM_OF_DELIMITERS = 30


def calc_height(img_gray):
    """
    Height calculation with pattern matching
    """
    img_gray_height = img_gray[65:129, :]
    dict_digits = {}
    for i in list(range(10))+["dot"]:
        template = cv2.imread(f"images/{i}.png", 0)
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


def check_record(img_gray):
    """
    Confirmation of termination by recognition of record image
    """
    template = cv2.imread("images/record.png", 0)
    res = cv2.matchTemplate(
        img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= THRESHOLD)
    if len(loc[1]) > 0:
        return True
    else:
        return False


class AnimalTower(gym.Env):
    def __init__(self):
        print("Initializing...", end=" ", flush=True)
        a = np.linspace(0, 7, 8)
        b = np.linspace(0, 1079, 32)
        self.ACTION_MAP = np.array([v for v in itertools.product(a, b)])
        self.action_space = gym.spaces.Discrete(256)
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=(288, 512))
        self.reward_range = [-1, 1]
        self.prev_height = 0
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
        print("Done")
        print("-"*NUM_OF_DELIMITERS)

    def reset(self):
        print("Resetting...", end=" ", flush=True)
        # Tap the Reset button
        self._tap(RESET_BUTTON_COORDINATES, WAITTIME_AFTER_RESET)
        img_gray = cv2.imread("test.png", 0)
        img_gray_resized = cv2.resize(img_gray, dsize=(512, 288))
        observation = img_gray_resized
        # Returns obs after start
        print("Done")
        return observation

    def step(self, action_index):
        # Perform Action
        action = self.ACTION_MAP[action_index]
        print(
            f"Action being performed({action[0]:.0f}, {action[1]})...", end=" ", flush=True)
        for _ in range(int(action[0])):
            self._tap(ROTATE_BUTTON_COORDINATES, _WAITTIME_AFTER_ROTATION)
        sleep(WAITTIME_AFTER_ROTATION)
        self._tap((action[1], 800), WAITTIME_AFTER_DROP)
        print("Done")

        # Generate obs and reward, done flag, and return
        self.driver.save_screenshot("test.png")
        img_gray = cv2.imread("test.png", 0)
        height = calc_height(img_gray)
        if check_record(img_gray):
            observation = cv2.resize(img_gray, dsize=(512, 288))
            reward = -1
            done = True
            print("Game over")
        else:
            while height is None:
                sleep(POLLONG_INTERVAL)
                self.driver.save_screenshot("test.png")
                img_gray = cv2.imread("test.png", 0)
                height = calc_height(img_gray)
            if height != self.prev_height:
                observation = cv2.resize(img_gray, dsize=(512, 288))
                reward = 1
                done = False
                print(f"Height update: {height}m")
            else:
                observation = cv2.resize(img_gray, dsize=(512, 288))
                reward = 0
                done = False
                print("No height update")
            self.prev_height = height
        print(f"return observation, reward({reward}), done({done}), {{}}")
        print("-"*NUM_OF_DELIMITERS)
        return observation, reward, done, {}

    def render(self):
        pass

    def _tap(self, coordinates, waittime):
        """
        Tap
        """
        while True:
            try:
                self.operations.w3c_actions.pointer_action.move_to_location(
                    coordinates[0], coordinates[1])
                self.operations.w3c_actions.pointer_action.pointer_down()
                self.operations.w3c_actions.pointer_action.pause(TAP_TIME)
                self.operations.w3c_actions.pointer_action.release()
                self.operations.perform()
                sleep(waittime)
                break
            except InvalidElementStateException:
                # 座標がオーバーフローしたとき?
                print("エラー?")
            except WebDriverException:
                # 謎
                print("謎エラー")


if __name__ == "__main__":
    for i in range(100):
        print(f"{i+1}回目ループ")
        if os.path.exists("half.zip"):
            model = A2C.load("half.zip", AnimalTower(),
                             print_system_info=True)
        else:
            model = A2C("MlpPolicy", AnimalTower(), verbose=1,
                        tensorboard_log="./a2c_cartpole_tensorboard/")
        print(model.get_parameters())
        model.learn(total_timesteps=20)
        model.save("half")
    # model = PPO('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./dtb_ppo/")
    # model.learn(total_timesteps=10_000)
    # model.save("kuu")
