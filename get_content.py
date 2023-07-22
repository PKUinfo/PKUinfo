#!/bin/python
import requests
import re
from bs4 import BeautifulSoup
import os
import csv
import easyocr

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
    save_dir = "/mnt/d/projectB/py/add/outcome/"
    if os.path.exists(save_dir):
        delete_directory(save_dir)
        os.makedirs(save_dir, exist_ok=True)
        return save_dir
    else:
        os.makedirs(save_dir, exist_ok=True)
        return save_dir


def ocr(img_dir,c,save_dir):
        
    reader = easyocr.Reader(
        ['ch_sim','en'],
        gpu = False,
        detect_network= 'craft',
        download_enabled= False,
        model_storage_directory= '/mnt/d/projectB/py/add/model/'
    )
    try:
        result = reader.readtext(img_dir)

    except:
        return
    
    for i in result:
        with open(save_dir+"{}.txt".format(c),'a',encoding = 'utf-8') as f:
            #f.write(i[1]+' '+str(i[2]) + '\n')           #最后输出ptxt
            f.write(i[1]+'\n')


def get_text(url,c,save_dir):   #传入网址和文件名
    
    #获取并格式化
    r = requests.get(url)
    r.encoding = 'utf-8'
    html_doc = r.text

    #文字获取部分
    s = BeautifulSoup(html_doc,features='lxml')
    doc = s.find_all("p")                         #只保留有p的部分

    for item in doc:
        ptxt = re.sub('\s',' ',item.get_text())
        with open(save_dir+"{}.txt".format(c),'a',encoding = 'utf-8') as f:
            f.write(ptxt + '\n')                  #最后输出ptxt

    print("find doc ok!!")
    
def get_img(url,c,save_dir):
    
    #获取并格式化
    r = requests.get(url)
    r.encoding = 'utf-8'
    html_doc = r.text

    #图片获取部分
    s2 = BeautifulSoup(html_doc,"html.parser") 
    img = s2.find_all("img")

    i = 0
    for item in img:
        src=''
        print ('')
        print ('.........img begin .......')
        try:
            src = item["src"]                   #有些存到了src,有些存到了data-src,判断一下
        except:
            try:
                src = item["data-src"]
            except:
                src = item["id"]
                
        if "https" not in src:                #把不是链接的抛掉
            continue
        
        if '=gif' in src:
            continue
        
        print (str(c)+src)
        
        ocr(src,c,save_dir)
        
        print ('.........img end .......')

        # resp_img = requests.get(src)
        # with open(save_dir+"img{}.jpg".format(i), "wb") as f:   #图片命名为img0
        #     f.write(resp_img.content)                           #保存content部分
        #     i = i + 1


def main():

    c = 0           
    save_dir = set_directory()
    
    with open("/mnt/d/projectB/py/add/urllist.csv", 'r' ,encoding = 'utf-8-sig') as f:    #utf-8会自动补前缀
        reader = csv.reader(f)
        for row in reader:
            print(str(c) + ':' + row[0])               #取列表第一个元素,不然不是链接形式
            url = row[0]
            
            # if c!=13:
            #     c=c+1
            #     continue
            
            get_text(url,c,save_dir)
            get_img(url,c,save_dir)
            
            c = c + 1            
    
main()

