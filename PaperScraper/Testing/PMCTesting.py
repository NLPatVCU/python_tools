from websites.PMC import PMC
from selenium import webdriver
import json
from pprint import pprint

# Test articles
"""
 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3418173/
 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5147414/
"""

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
t = PMC(driver)

dict = t.extract("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5147414/")
print(json.dumps(dict, indent=4))

driver.quit()
