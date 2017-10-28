#! /usr/bin/env python3
#-*-coding:utf-8 -*-
#write by cc

import requests
from bs4 import BeautifulSoup
import re
import time

req_header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

pat_title = "<title>(.*) - Gene - NCBI</title>"
r1 = re.compile(pat_title)
pat_mRNA = 'mRNA and Protein\(s\).*?(<ol>.*?</ol>)'
r2 = re.compile(pat_mRNA, re.S) #使.匹配换行符\n

to_file = open("all.mRNAs", "w") #写入文件

def onePage(url):
    #print("url=%s" %url)
    req1 = requests.get(url, headers = req_header)
    list1 = r1.findall(req1.text)
    title = list1[0]
    list_all = [] #存储mRNA的值

    if "No items found" in title: #没有搜寻结果
        pass
    elif(title ==  url.split("=")[-1]): #提供多个搜索结果
        pass
    else: #只有1个搜索结果
        html_mRNA = r2.findall(req1.text)[0]
        soup = BeautifulSoup(html_mRNA, 'lxml')
        for i in soup.find_all("li"):
            label_p = str(i.p)
            list_temp = re.compile("<a.*?>(.*?)</a>").findall(label_p)
            for i in list_temp:
                list_all.append(i)

    line = ','.join([req1.url, title])
    if(list_all):
        str1 = ""
        for i in list_all:
            str1 = str1 + i + ","
        str1 = str1[:-1]
        line = line + ',' + str1
    to_file.write(line + '\n')
    print("--------------------")

from_file = open("all.pages", "r")
list1 = from_file.readlines()
for line in list1:
    print("processing %d" %(list1.index(line) + 1))
    url = line.strip("\n")
    onePage(url)
    #休眠1s
    time.sleep(1)

from_file.close()
to_file.close()