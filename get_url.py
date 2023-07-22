from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import csv
import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

add = []

def delete_directory(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)  # 删除文件

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)   # 删除子目录

    os.rmdir(directory)   # 删除目录
    
def set_directory():
    save_dir = "/mnt/d/projectB/py/add/"
    if os.path.exists(save_dir):
        return save_dir
    
    else:
        os.makedirs(save_dir, exist_ok=True)
        return save_dir

def get_url(name):
    driver = webdriver.Chrome()
    # 进入网页
    driver.get("https://weixin.sogou.com/")
    
    driver.find_element(By.ID, 'query').send_keys(name)
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()  # 使用CSS选择器定位元素
    driver.find_element(By.CLASS_NAME, 'swz2').click()
    driver.find_element(By.XPATH, "//a[@target='_blank' and contains(@uigs, 'account_article_0')]").click() 
    time.sleep(10)
    #driver.find_element(By.TAG_NAME,'body').send_keys(Keys.DOWN)

    for window_handle in driver.window_handles:
        # 切换到窗口
        driver.switch_to.window(window_handle)
        # 获取当前窗口的URL
        url = driver.current_url
        print(url)
        if 'mp.weixin.qq' in url:
            current_url = driver.current_url
            print("当前页面的URL:", current_url)
            
            redirected_url = driver.execute_script("return window.location.href")
            
            # headers = {'User-Agent': 'Mozilla/5.0 (windows NT 10.0;WOW64) AppleWebkit/537'}
            # response = requests.get(current_url,headers=headers)
            # redirected_url = response.url
            print("重定向后的URL:", redirected_url)
            
            add.append(redirected_url)

    print('\n....done....')
    driver.quit()
    
def main():
    
    set_directory()
    
    with open("/mnt/d/projectB/py/add/namelist2.csv", 'r' ,encoding = 'utf-8') as f:  
        reader = csv.reader(f)
        for row in reader:
            name = row[0]
            
            get_url(name)
    
    with open("/mnt/d/projectB/py/add/urllist.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[url] for url in add])


main()
