import os
import time

from pykeyboard import PyKeyboard
from pymouse import *
from selenium import webdriver
import numpy as np

options = webdriver.ChromeOptions()
prefs = {
    "download.prompt_for_download": False,
    'download.default_directory':
        '/Users/huang/Desktop/workpython/jayin-python-app/src/selenium/dianping/shop_lists',
    # 下载目录
    "plugins.always_open_pdf_externally": True,
    'profile.default_content_settings.popups': 0,  # 设置为0，禁止弹出窗口
    # 'profile.default_content_setting_values.images': 2,#禁止图片加载
}
options.add_experimental_option('prefs', prefs)

# chrome可以直接保存为一个单独的mhtml文档，但是chrome是默认关闭状态
# options.add_argument('--save-page-as-mhtml')

executable_path = "%s/../chromedriver" % os.path.dirname(__file__)
driver = webdriver.Chrome(executable_path, chrome_options=options)  # 选择chrom或firefox浏览器

url = "http://www.dianping.com/search/keyword/7/10_%E8%81%9A%E9%A4%90/o2/"
# url = "https://blog.csdn.net/xc_zhou/article/details/86247557"
driver.get(url)

# 拉动下拉滚动条，下拉800,csdn网页阅读更多按钮要在当前屏幕显示，不然下边点击操作会报错
driver.execute_script("window.scroll(0, 800);")
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/ul/li[3]/a').click()

exit()


def save_current_page(file_name):
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
    for key in file_name:
        k.tap_key(key)

    time.sleep(2)
    enter_key = "Return"
    k.press_key(enter_key)
    k.release_key(enter_key)
    # 如果文件已存在，再次按下enter，默认是否选项，即不重复下载
    time.sleep(30)
    # k.tap_key(k.numpad_keys[5],3) #–点击小键盘5,3次
    left_key = "Escape"
    k.press_key(left_key)
    k.release_key(left_key)
    time.sleep(1)
    k.press_key(left_key)
    k.release_key(left_key)

    # 预估下载时间，后期根据实际网速调整
    time.sleep(5)


shop_list_page_idx = 1
current_page = "shop_list_%d" % shop_list_page_idx
# save_current_page(current_page)

time.sleep(3)

for idx in range(1, 16)[:1]:
    shop_xpath = '//*[@id="shop-all-list"]/ul/li[%s]/div[2]/div[1]/a' % idx
    driver.find_element_by_xpath(shop_xpath).click()
    time.sleep(np.random.randint(30, 100) / 1000)
    print("current_url", driver.current_url)

# 关闭webdriver
driver.close()
