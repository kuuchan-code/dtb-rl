#!/usr/bin/env python3
from appium import webdriver
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
WAITTIME_AFTER_DROP = 7
ABOUT_WAITTIME_AFTER_DROP = 3
WAITTIME_AFTER_RESET = 7
POLLONG_INTERVAL = 1
WAITTIME_AFTER_ROTATION = 0.5
_WAITTIME_AFTER_ROTATION = 0.005
TAP_TIME = 0.001
RESET_BUTTON_COORDINATES = 200, 1755
ROTATE_BUTTON_COORDINATES = 500, 1800
NUM_OF_DELIMITERS = 30
TRAIN_WIDTH = 256
TRAIN_SIZE = int(TRAIN_WIDTH/1920*1080), TRAIN_WIDTH
NUM_OF_DIV = 32
SS_NAME = "ss.png"
OBSERVATION_NAME = "observation.png"


def get_heght(img_gray):
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
    if not(height):
        height = 0
    return float(height)


def get_animal_num(img_gray):
    img_gray_num = img_gray[264:328, :]
    cv2.imwrite("tesst.png", img_gray_num)
    dict_digits = {}
    for i in list(range(10)):
        template = cv2.imread(f"images/{i}.png", 0)
        res = cv2.matchTemplate(
            img_gray_num, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 80)
        print(loc, i)
        for y in loc[1]:
            dict_digits[y] = i
    animal_num = ""
    for key in sorted(dict_digits.items()):
        animal_num += str(key[1])
    if not(animal_num):
        animal_num = 0
    return int(animal_num)


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
    act_min = 0
    act_max = 1

    def __init__(self):
        print("Initializing...", end=" ", flush=True)
        # 連続値の座標(?)
        self.action_space = gym.spaces.Box(
            self.act_min, self.act_max, shape=(1,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=TRAIN_SIZE[::-1])
        self.reward_range = [-10, 10]
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
        self.driver.save_screenshot(SS_NAME)
        img_gray = cv2.imread(SS_NAME, 0)
        img_gray_resized = cv2.resize(img_gray, dsize=TRAIN_SIZE)
        self.prev_height = get_heght(img_gray)
        observation = img_gray_resized
        # Returns obs after start
        print("Done")
        cv2.imwrite(OBSERVATION_NAME, observation)
        return observation

    def step(self, action):
        # Perform Action
        x = np.clip(action, self.act_min, self.act_max)[0] * 1080
        x.astype(int)
        print(f"Action({x})")
        self._tap((x, 800), WAITTIME_AFTER_DROP)
        # Generate obs and reward, done flag, and return
        for i in range(ABOUT_WAITTIME_AFTER_DROP):
            self.driver.save_screenshot(SS_NAME)
            img_gray = cv2.imread(SS_NAME, 0)
            height = get_heght(img_gray)
            print(height, self.prev_height)
            img_gray_resized = cv2.resize(img_gray, dsize=TRAIN_SIZE)
            observation = img_gray_resized
            if check_record(img_gray):
                print("Game over")
                print("return observation, -1, True, {}")
                print("-"*NUM_OF_DELIMITERS)
                cv2.imwrite(OBSERVATION_NAME, observation)
                return observation, -10, True, {}
            elif height != self.prev_height:
                print(f"Height update: {height}m")
                print("return observation, 1, False, {}")
                print("-"*NUM_OF_DELIMITERS)
                self.prev_height = height
                cv2.imwrite(OBSERVATION_NAME, observation)
                return observation, height, False, {}
            else:
                pass
            sleep(POLLONG_INTERVAL)
        print("No height update")
        print("return observation, 0, False, {}")
        print("-"*NUM_OF_DELIMITERS)
        cv2.imwrite(OBSERVATION_NAME, observation)
        return observation, height, False, {}

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
    at = AnimalTower()
