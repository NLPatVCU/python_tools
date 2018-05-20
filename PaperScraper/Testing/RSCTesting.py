from websites.RSC import RCS
from selenium import webdriver
import json

# http://pubs.rsc.org/en/content/articlehtml/2017/CC/C7CC04465H
# http://pubs.rsc.org/en/content/articlehtml/2017/cc/c7cc04949h

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
#driver = webdriver.Chrome("/home/andriy/Documents/gitprojects/NLP-Lab/Tools/PaperScraper/drivers/chromedriver",chrome_options=options)
t = RCS(driver)

dict = t.extract("http://pubs.rsc.org/en/content/articlehtml/2017/cc/c7cc04949h")

print(json.dumps(dict, indent=4))
driver.quit()
