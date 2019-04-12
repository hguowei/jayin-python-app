import shutil
import sys
import time
import os


def check_driver():
    dest_path = "/usr/local/bin/chromedriver"
    if not os.path.exists(dest_path):
        current_directory = os.path.dirname(__file__)
        sys.path.append(current_directory)
        shutil.copy2("%s/chromedriver" % current_directory, dest_path)


check_driver()

from selenium import webdriver

wd = webdriver.Chrome()
wd.get("https://www.baidu.com")  # 打开百度浏览器
wd.find_element_by_id("kw").send_keys("selenium")  # 定位输入框并输入关键字
wd.find_element_by_id("su").click()  # 点击[百度一下]搜索
time.sleep(3)  # 等待3秒
wd.quit()  # 关闭浏览器
