from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from PIL import Image
from io import BytesIO
import json
import logging
import random
import string

invalidText = [
  "该 分 享 文 件 已 过 期",
  "此 链 接 分 享 内 容 可 能 因 为 涉 及 侵 权"
]

def selenium_check_validation(pan_url):
  logging.warning("validating " + pan_url + "...")
  driver = webdriver.Chrome()
  driver.set_window_size(1120, 550)
  driver.get(pan_url)
  driver.refresh()
  if "链接不存在" in driver.title:
    logging.warning("链接不存在")
    driver.quit()
    return "invalid"
  else:
    png = driver.get_screenshot_as_png()
    driver.quit()
    img = Image.open(BytesIO(png))
    text = pytesseract.image_to_string((img), lang='chi_sim')
    if not validate_text(text):
      return "continue"
    logging.warning("链接有效")
    if "请 输 入 提 取 码" in text:
      return "needpassword"
    return "stop"
  
def validate_text(text):
  if any(map(lambda invalid: invalid in text, invalidText)):
    return False
  return True

if __name__=="__main__":
  data = json.load(open('baidu_raw.json'))
  for main_page in data:
    new_dict ={}
    host_url = main_page['page']
    links = main_page['links']
    for link in links:
      pan_url = link['link']
      validation = selenium_check_validation(pan_url)
      # nice
      if validation == "stop":
        new_dict["page"] = host_url
        new_dict["url"] = link['link']
        with open("baidu_raw" + ''.join(random.choice(string.digits) for _ in range(4)) + ".json", "w") as fd:
          json.dump(new_dict,fd)
      # need password
      elif validation == "needpassword":
        new_dict["page"] = host_url
        new_dict["url"] = link['link']
        new_dict["mode"] = "提取码"
        with open("baidu_raw" + ''.join(random.choice(string.digits) for _ in range(4)) + ".json", "w") as fd:
          json.dump(new_dict,fd)
