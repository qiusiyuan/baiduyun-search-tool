from subprocess import call
import os
if __name__=="__main__":
  search_item = input("输入您的词条:")
  os.environ['SEARCH_ITEM']=search_item
  call(["scrapy", "runspider", "baiduSearch.py", "-o", "baidu.json"])