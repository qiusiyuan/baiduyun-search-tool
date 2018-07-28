from subprocess import call
import os

if __name__=="__main__":
  search_item = input("输入您的词条:")
  os.environ['SEARCH_ITEM']=search_item
  try:
    os.remove("baidu.json")
  except:
    pass
  try:
    os.remove("baidu_raw.json")
  except:
    pass
  call(["scrapy", "runspider", "baiduSearch.py", "-o", "baidu_raw.json"])

  print("Starting to validate baidu pan url......")
  call(["python3", "urlChecker.py"])


