import os
import time

from pykeyboard import PyKeyboard
from pymouse import *
from selenium import webdriver

options = webdriver.ChromeOptions()
prefs = {
    "download.prompt_for_download": False,
    'download.default_directory': 'C:/Users/Administrator/Desktop/1/',  # 下载目录
    "plugins.always_open_pdf_externally": True,
    'profile.default_content_settings.popups': 0,  # 设置为0，禁止弹出窗口
    # 'profile.default_content_setting_values.images': 2,#禁止图片加载
}
options.add_experimental_option('prefs', prefs)

# chrome可以直接保存为一个单独的mhtml文档，但是chrome是默认关闭状态
# 打开另存为mhtml功能
options.add_argument('--save-page-as-mhtml')

executable_path = "%s/../chromedriver" % os.path.dirname(__file__)
driver = webdriver.Chrome(executable_path, chrome_options=options)  # 选择chrom或firefox浏览器

url = "http://www.dianping.com/search/keyword/7/10_%E8%81%9A%E9%A4%90/o2/"
# url = "https://blog.csdn.net/xc_zhou/article/details/86247557"
driver.get(url)

# 拉动下拉滚动条，下拉800,csdn网页阅读更多按钮要在当前屏幕显示，不然下边点击操作会报错
driver.execute_script("window.scroll(0, 800);")
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/ul/li[3]/a').click()
# --------------------------方法1-------------------------------------
##有些网站需要点击一下页面，才能进行保存，比如csdn
# #鼠标移动到某一位置，左键点击一下
# windll.user32.SetCursorPos(100, 100)#坐标值
# time.sleep(0.05)
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
# # # 模拟键盘操作
# win32api.keybd_event(17, 0, 0, 0)           # 按下ctrl
# win32api.keybd_event(65, 0, 0, 0)           # 按下a
# win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放a
# win32api.keybd_event(83, 0, 0, 0)           # 按下s
# win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放s
# win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放ctrl
# #加上休眠时间等待弹框的出现
# time.sleep(2)
# win32api.keybd_event(13, 0, 0, 0)           # 按下enter
# win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放enter
# #如果文件已存在，会在弹出一个提示框，提示是否要替换，默认是否选项，
# #按下键盘小箭头左移，选择是，然后再次按下enter，
# time.sleep(2)#加上休眠时间等待弹框的出现
# win32api.keybd_event(37, 0, 0, 0)           # 按下小箭头左移
# win32api.keybd_event(37, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放小箭头左移
# time.sleep(0.5)
# win32api.keybd_event(13, 0, 0, 0)           # 按下enter
# win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放enter

# --------------------------方法2-------------------------------------
# 鼠标操作
m = PyMouse()
'''
m.click(x,y,button,n) –鼠标点击
x,y –是坐标位置
buttong -1表示左键，2表示点击右键
n –点击次数，默认是1次，2表示双击
'''
# 有些网站需要点击一下页面，才能进行保存，比如csdn
m.click(100, 100, 1, 1)
# #键盘操作
k = PyKeyboard()
control_key = "Command"
k.press_key(control_key)  # 按下ctrl键
# k.press_key('a') #按下a键
# k.release_key('a')#释放a键
k.press_key('s')
k.release_key('s')
k.release_key(control_key)
# 加上休眠时间等待弹框的出现
time.sleep(2)
enter_key = "Return"
k.press_key(enter_key)
k.release_key(enter_key)
# 如果文件已存在，再次按下enter，默认是否选项，即不重复下载
time.sleep(2)
# k.tap_key(k.numpad_keys[5],3) #–点击小键盘5,3次
left_key = "Escape"
k.press_key(left_key)
k.release_key(left_key)
time.sleep(1)
k.press_key(left_key)
k.release_key(left_key)

# 预估下载时间，后期根据实际网速调整
time.sleep(5)
# 关闭webdriver
driver.close()
