from websites.ACS import ACS
from selenium import webdriver
from pprint import pprint

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
#driver = webdriver.Chrome("/home/andriy/Documents/gitprojects/NLP-Lab/Tools/PaperScraper/drivers/chromedriver",chrome_options=options)
t = ACS(driver)

pprint(t.extract("https://pubs.acs.org/doi/full/10.1021/la049463z"))

driver.quit()
