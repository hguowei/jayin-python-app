from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import codecs
import os
import time
import numpy as np
executable_path = "%s/../chromedriver" % os.path.dirname(__file__)
driver = webdriver.Chrome(executable_path)  # 选择chrom或firefox浏览器

driver.get("http://www.guyitai.net/stock/bankdata/")

e1 = driver.find_element_by_xpath("//a[@value='0002']")  # 选择地区：浙江
e1.click()
e2 = driver.find_element_by_xpath("//a[@value='0002-0001']")  # 选择城市：杭州
WebDriverWait(driver, 10).until(expected_conditions.visibility_of(e2))  # 等待页面
e2.click()
count = 0
while count < 10:
    count += 1
    locals()['page_' + str(count)] = driver.page_source
    filename = str()
    with codecs.open('page_' + str(count) + '.txt', 'w', encoding='utf-8') as f:  # 保存网页源代码
        f.write(locals()['page_' + str(count)])
    try:
        rand = np.random.randint(0, 1)
        print("rand", rand)
        time.sleep(1.2)
        clickbutton = driver.find_element_by_link_text('下一页')
        clickbutton.click()
    except:
        break
driver.close()  # 关闭浏览器

# 利用下载的源代码可利用BeautifulSoup进行html数据抓取
