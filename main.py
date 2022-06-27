from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from time import sleep
from PIL import Image
import pytesseract


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
        I = Image.open('test.png')
        I = I.convert("L").point(lambda x: 255 if x < 255 else 0, mode="1")
        I = I.crop((0,50,500,450))
        # print(pytesseract.image_to_string(I))
        print(pytesseract.image_to_string(I, lang="jpn", config="digits --psm 6").split()[0])
        sleep(1)
except KeyboardInterrupt:
    driver.quit()