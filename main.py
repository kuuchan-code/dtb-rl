#!/usr/bin/env python3
from appium import webdriver
from time import sleep
import cv2
import numpy as np


caps = {}
caps["platformName"] = "android"
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:newCommandTimeout"] = 3600
caps["appium:connectHardwareKeyboard"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

try:
    while True:
        driver.save_screenshot('test.png')
        img_rgb = cv2.imread("test.png")
        img_rgb = img_rgb[65:129, 0:1080, :]
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        dict_digits = {}
        for i in list(range(10))+["dot"]:
            template = cv2.imread("digits/"+str(i)+".png",0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            threshold = 0.99
            loc = np.where(res >= threshold)
            if len(loc[1]) != 0:
                for y in loc[1]:
                    dict_digits[y] = i
            for pt in zip(*loc[::-1]):  
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        height = ""
        for key in sorted(dict_digits.items()):
            if key[1] == "dot":
                height += "."
            else:
                height += str(key[1])
        print(height)
        sleep(1)
except KeyboardInterrupt:
    driver.quit()