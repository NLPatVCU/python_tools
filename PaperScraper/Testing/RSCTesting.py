from PaperScraper.websites.RSC import RCS
from selenium import webdriver
from pprint import pprint

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
#driver = webdriver.Chrome("/home/andriy/Documents/gitprojects/NLP-Lab/Tools/PaperScraper/drivers/chromedriver",chrome_options=options)
t = RCS(driver)

pprint(t.extract("http://pubs.rsc.org/en/content/articlehtml/2017/cc/c7cc04949h"))

driver.quit()
