from PaperScraper.websites.Springer import Springer
from selenium import webdriver
import json


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
#driver = webdriver.Chrome("/home/andriy/Documents/gitprojects/NLP-Lab/Tools/PaperScraper/drivers/chromedriver",chrome_options=options)
t = Springer(driver)

dict = t.extract("https://link.springer.com/article/10.1007/s13187-016-1142-y")

print(json.dumps(dict, indent=4))
driver.quit()