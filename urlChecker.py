from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import logging
import random
import string

def selenium_check_validation(pan_url):
  logging.warning("validating " + pan_url + "...")
  driver = webdriver.PhantomJS()
  driver.set_window_size(1120, 550)
  driver.get(pan_url)
  driver.refresh()
  if "链接不存在" in driver.title:
    logging.warning("链接不存在")
    return False
  else:
    logging.warning("链接有效")
    return True
  driver.quit()

if __name__=="__main__":
  data = json.load(open('baidu_raw.json'))
  for main_page in data:
    new_dict ={}
    host_url = main_page['page']
    links = main_page['links']
    for link in links:
      pan_url = link['link']
      validation = selenium_check_validation(pan_url)
      if validation:
        if not new_dict:
          new_dict["page"] = host_url
          new_dict["links"] = [{"link":pan_url}]
        else:
          new_dict["links"].append({"link":pan_url})
    if new_dict:
      with open("baidu_raw" + ''.join(random.choice(string.digits) for _ in range(4)) + ".json", "w") as fd:
        json.dump(new_dict,fd)


