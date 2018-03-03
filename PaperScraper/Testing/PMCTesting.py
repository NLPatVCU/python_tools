from websites.PMC import PMC
from selenium import webdriver
from pprint import pprint

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome("/home/andriy/Documents/gitprojects/NLP-Lab/Tools/PaperScraper/drivers/chromedriver",chrome_options=options)
t = PMC(driver)

pprint(t.extract("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3418173/"))

driver.quit()