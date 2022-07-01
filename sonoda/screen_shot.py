#!/usr/bin/env python3
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import WebDriverException


caps1 = {
    "platformName": "Android",
    "appium:udid": "localhost:55436",
    "appium:ensureWebviewHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:newCommandTimeout": 3600,
    "appium:connectHardareKeyboard": True
}
try:
    # グローバル変数として定義
    print("デバイス1接続中")
    DRIVER1 = webdriver.Remote(
        "http://localhost:4723/wd/hub", caps1)

    OPERATIONS = ActionChains(DRIVER1)
except WebDriverException as e:
    print("端末に接続できない???")
    raise e

caps2 = caps1.copy()
caps2["appium:udid"] = "CB512C5QDQ"
print(caps1, caps2)

try:
    # グローバル変数として定義
    print("デバイス2接続中")
    DRIVER2 = webdriver.Remote(
        "http://localhost:4723/wd/hub", caps2)

    OPERATIONS = ActionChains(DRIVER2)
except WebDriverException as e:
    print("端末に接続できない???")
    raise e

try:
    while True:
        DRIVER1.save_screenshot(input("デバイス1スクショの保存先: "))
        DRIVER2.save_screenshot(input("デバイス2スクショの保存先: "))
except KeyboardInterrupt:
    print("キーボード割り込み")
