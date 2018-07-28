# -*- coding: utf-8 -*-
from urllib.parse import urlencode, quote
import urllib 
import requests
from lxml import html
import time
import re
from bs4 import BeautifulSoup
import chardet
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
# name = "baiduyun"
# search_item_string = "joker game百度云"
# search_item_encode = quote(search_item_string)
# main_baidu_search_url = "http://www.baidu.com/s?wd="
# start_urls = [main_baidu_search_url + search_item_encode]
# valid_urls = []
# url = start_urls[0]
# my_headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",  
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",  
# "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"  
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",  
# "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"  
      
# ]
# randdom_header=random.choice(my_headers)  
  
# req=urllib.request.Request(url)  
# req.add_header("User-Agent",randdom_header)  
# req.add_header("Host","blog.csdn.net")  
# req.add_header("Referer","http://blog.csdn.net/")  
# req.add_header("GET",url)  

# content=urllib.request.urlopen("http://pan.baidu.com/s/1hrP6jm0").read() 
#page =  requests.get("http://pan.baidu.com/s/1hrP6jm0", headers=hearders)
#print(page.status_code)
#content= page.content

#soup = BeautifulSoup(content, 'html.parser')
#parent 1
#jj = soup.find('div', {"class","error-img"})
#print(jj)
driver = webdriver.Chrome()
#driver.set_window_size(1120, 550)
driver.get("http://pan.baidu.com/s/1eSfTvME")
wait = WebDriverWait(driver, 10)
driver.refresh()
# with open("source.txt","w") as fd:
#   fd.write(driver.page_source)
#wait.until(EC.element_to_be_clickable((By.XPATH, ".//a[@href='http://pan.baidu.com/s/1eSfTvME']"))).click()
#second_window = driver.window_handles[1]
#driver.switch_to.window(second_window)
#wait.until(EC.visibility_of_element_located((By.XPATH, ".//a[@href='//pan.baidu.com/']")))

if "链接不存在" in driver.title:
  print("not exist")
with open("source.txt","w") as fd:
  fd.write(driver.page_source)