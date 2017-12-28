from urllib.parse import urlencode, quote
import scrapy
import time
import re
import logging

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


  def _handle_error(self, failure):
    logging.warning("Request failed: %s" % failure.request)

  def _search_baiduyun_link_call(self, block_link):
    yield scrapy.Request(url=block_link, callback=self.search_baiduyun_link)

  def search_baiduyun_link(self, response):
    all_links = response.xpath(".//a/@href").extract()
    baidu_yun_link = self.baiduyun_link_filter(all_links)
    if len(baidu_yun_link) > 0:
      yield  {"page":response.url, "links": baidu_yun_link}

  def baiduyun_link_filter(self, link_list):
    baidu_yun_link =[]
    pattern = r"http(s?)(.*?)pan.baidu.com(.*?)\/s\/(.*?)"
    prog = re.compile(pattern)
    for link in link_list:
      if prog.match(link):
        baidu_yun_link.append(link)
    return baidu_yun_link
