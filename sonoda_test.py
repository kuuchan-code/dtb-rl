#!/usr/bin/env python3
from appium import webdriver
from time import sleep
import numpy as np
import cv2
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

caps = {}
caps["platformName"] = "android"
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:newCommandTimeout"] = 3600
caps["appium:connectHardwareKeyboard"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
print(driver)
# actions = TouchAction(driver)
THRESHOLD = 0.99


actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(
    driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))


try:
    while True:
        driver.save_screenshot('test.png')
        img_bgr = cv2.imread("test.png")
        img_bgr = img_bgr[65:129, 0:300, :]
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        dict_digits = {}
        for i in list(range(10))+["dot"]:
            template = cv2.imread(f"digits/{i}.png", 0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= THRESHOLD)
            # print(loc[1])
            for y in loc[1]:
                dict_digits[y] = i
            for pt in zip(*loc[::-1]):
                cv2.rectangle(
                    img_bgr, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        height = ""
        for key in sorted(dict_digits.items()):
            if key[1] == "dot":
                height += "."
            else:
                height += str(key[1])
        # タップしてみる
        actions.w3c_actions.pointer_action.move_to_location(496, 954)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        print(height)
        sleep(1)

except KeyboardInterrupt:
    driver.quit()
