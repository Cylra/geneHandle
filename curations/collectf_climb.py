#! /usr/bin/env python3
#-*-coding:utf-8 -*-
#write by cc
'''
    获取页面view全部链接中的Transcription Factor Binding Sites
'''

import requests
from bs4 import BeautifulSoup
import re
import os
import time
import threading
import subprocess
import signal

basic_file = "all.pages"
basic_url = "http://www.collectf.org/browse/list_all_curations/"
dst_file = "allGene.info"

#获取全部页面
def genURLFile():
    r = requests.get(basic_url)
    soup = BeautifulSoup(r.content, "lxml")
    f = open(basic_file, "w")
    for i in soup.find_all("a", href=re.compile("view_curation")):
        f.write("http://www.collectf.org" + i["href"] + "\n")
    f.close()

#获取一个页面需要的内容并写入文件
def getOneWebInfo(oneWeb, f_dst):
    def writeTitle():
        title = soup.find_all("dd")[1].contents[0]
        f_dst.write(re.sub(r"[\n  []", "", str(title)) + "\n")
    def writeContent():
        for i in soup.find_all("div", class_="box shaded-background")[0]:
            if(i.name == "span"):
                f_dst.write(i.string + "\n")

    r = requests.get(oneWeb)
    soup = BeautifulSoup(r.content, "lxml")
    f_dst.write(oneWeb + "\n")
    writeTitle()
    writeContent()
    f_dst.write("\n")

#信号处理函数,用于显示处理进度
def speed(a, b):
    print("当前处理的网页为: " + str(cur) + "/" + str(rows))

if(not os.path.exists('./' + basic_file)):
    genURLFile()

output = subprocess.check_output("wc -l " + basic_file, shell = True).decode("utf-8")
rows = output.split()[0] #更正行数统计方法
cur = 0
#注册信号
signal.signal(signal.SIGTSTP, speed)  

#file operation
f = open(basic_file, "r")
f_dst = open(dst_file, "w")
oneWeb = f.readline().strip('\n')
pid = os.getpid() #提前获得进程id
while(oneWeb):
    cur += 1
    os.kill(pid, signal.SIGTSTP) #避免循环中多次调用函数,增加负担
    getOneWebInfo(oneWeb, f_dst)
    #final
    oneWeb = f.readline().strip('\n')

f.close()
f_dst.close()