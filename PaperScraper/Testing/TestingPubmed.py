from aggregators.PubMedAggregator import PubMedAggregator
from selenium import webdriver
from pprint import pprint
import os

options = webdriver.ChromeOptions()
options.add_argument('headless')
path = os.path.abspath(__file__)
driver = webdriver.Chrome("/home/andriy/Documents/gitprojects/NLP-Lab/Tools/PaperScraper/drivers/chromedriver",chrome_options=options)

pm = PubMedAggregator(driver)

pprint(pm.extract(20060075))
