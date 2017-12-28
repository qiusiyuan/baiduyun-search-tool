from urllib.parse import urlencode, quote
import scrapy
import time
import re
import requests
from lxml import html

class baiduyunSearch(scrapy.Spider):
  name = "baiduyun"
  search_item_string = "joker game百度云"
  search_item_encode = quote(search_item_string)
  main_baidu_search_url = "http://www.baidu.com/s?wd="
  start_urls = [main_baidu_search_url + search_item_encode]
  valid_urls = []

  def parse(self, response):
    block_link_xpath = ".//div[@class='result c-container ']//h3/a/@href"
    block_links_list = response.xpath(block_link_xpath).extract()
    print(len(block_links_list))
    for block_link in block_links_list:
      link_list = self.search_baiduyun_link(block_link)
      self.valid_urls.extend(link_list)
    for link in self.valid_urls:
      print(link)

  def search_baiduyun_link(self, main_url):
    try:
      page = requests.get(main_url, timeout=3)
      response = html.fromstring(page.text)
      all_links = response.xpath(".//a/@href")
      baidu_yun_link = self.baiduyun_link_filter(all_links)
      return baidu_yun_link
    except:
      print("cannot make connection to " + main_url)
      return []
      
  def baiduyun_link_filter(self, link_list):
    baidu_yun_link =[]
    pattern = r"http(s?)(.*?)pan.baidu.com(.*?)\/s\/(.*?)"
    prog = re.compile(pattern)
    for link in link_list:
      if prog.match(link):
        baidu_yun_link.append(link)
    return baidu_yun_link
