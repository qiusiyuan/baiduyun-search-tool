from urllib.parse import urlencode, quote
import scrapy
import time
import re
import logging
import requests
from lxml import html
from bs4 import BeautifulSoup

class baiduyunSearch(scrapy.Spider):
  name = "baiduyun"
  download_timeout = 3
  search_item_string = "joker game百度云"
  search_item_encode = quote(search_item_string)
  main_baidu_search_url = "http://www.baidu.com/s?wd="
  start_urls = [main_baidu_search_url + search_item_encode]

  def parse(self, response):
    block_link_xpath = ".//div[@class='result c-container ']//h3/a/@href"
    block_links_list = response.xpath(block_link_xpath).extract()
    print(len(block_links_list))
    for block_link in block_links_list:
      yield scrapy.Request(url=block_link, callback=self.search_baiduyun_link, errback=self._handle_error)
    
    next_page = None
    next_page_xpath = ".//div[@id='page']//a[@class='n']/@href"
    link_list = response.xpath(next_page_xpath).extract()
    for link in link_list:
      if link.endswith("page=1"):
        next_page = link
    if next_page:
      yield scrapy.Request(response.urljoin(next_page))

  def _search_baiduyun_link_call(self, block_link):
    yield scrapy.Request(url=block_link, callback=self.search_baiduyun_link)

  def search_baiduyun_link(self, response):
    all_links = response.xpath(".//a/@href").extract()
    baidu_yun_links = self.baiduyun_link_filter(all_links)
    if len(baidu_yun_links) > 0:
      yield  {"page":response.url, "links": baidu_yun_links}

  def baiduyun_link_filter(self, link_list):
    baidu_yun_link =[]
    pattern = r"http(s?)(.*?)pan.baidu.com(.*?)\/s\/(.*?)"
    prog = re.compile(pattern)
    for link in link_list:
      if prog.match(link):
        code = self._valid_baidu_yun_link(link)
        if code == 'good':
          baidu_yun_link.append({"link": link, "pw": ""})
        elif code == 'needpw':
          baidu_yun_link.append({"link": link, "pw": "needpw"})
    return baidu_yun_link
  
#####################################################################
# helper function
#####################################################################

  def _valid_baidu_yun_link(self, baidu_yun_link):
    """
    return 'invalid' 'needpw' 'good'
    """
    page = requests.get(baidu_yun_link)
    response = html.fromstring(page.text)
    error_xpath = ".//div[@class='error-img']"
    password_xpath = ".//dl[@class='pickpw clearfix']"
    if response.xpath(error_xpath):
      return 'invalid'
    elif response.xpath(password_xpath):
      return 'needpw'
    else:
      return 'good'

  def _handle_error(self, failure):
    logging.warning("Request failed: %s" % failure.request)

  