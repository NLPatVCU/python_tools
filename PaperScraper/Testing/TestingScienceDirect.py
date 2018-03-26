import os
from websites.ScienceDirect import ScienceDirect
from selenium import webdriver
import json

#https://www.sciencedirect.com/science/article/pii/S0144861713011806?via%3Dihub
#https://www.sciencedirect.com/science/article/pii/S0041008X08003888?via%3Dihub



options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome("/home/andriy/Documents/gitprojects/NLP-Lab/Tools/PaperScraper/drivers/chromedriver",chrome_options=options)
t = ScienceDirect(driver)

dict = t.extract("http://linkinghub.elsevier.com/retrieve/pii/S1549-9634(10)00005-5")

print(json.dumps(dict, indent=4))
# t.extract("https://www.sciencedirect.com/science/article/pii/S0041008X08003888?via%3Dihub")
#
# t.extract("facebook.com")

driver.quit()