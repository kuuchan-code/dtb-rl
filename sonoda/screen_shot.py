#!/usr/bin/env python3
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import WebDriverException


# caps = {}
# caps["platformName"] = "android"
# caps["appium:ensureWebviewsHavePages"] = True
# caps["appium:nativeWebScreenshot"] = True
# caps["appium:newCommandTimeout"] = 3600
# caps["appium:connectHardwareKeyboard"] = True
caps = {
    "platformName": "Android",
    "appium:ensureWebviewHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:newCommandTimeout": 3600,
    "appium:connectHardareKeyboard": True
}
try:
    # グローバル変数として定義
    print("ドライバ接続中")
    DRIVER = webdriver.Remote(
        "http://localhost:4723/wd/hub", caps)

    OPERATIONS = ActionChains(DRIVER)
    OPERATIONS.w3c_actions = ActionBuilder(
        DRIVER, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
except WebDriverException as e:
    print("端末に接続できない???")
    raise e

try:
    while True:
        DRIVER.save_screenshot(input("スクショの保存先: "))
except KeyboardInterrupt:
    print("キーボード割り込み")
