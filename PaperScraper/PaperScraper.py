from aggregators import PubMedAggregator
from websites.ScienceDirect import ScienceDirect
from selenium import webdriver
import os
"""A python module to scrape full papers with meta-data from leading online publishers"""

class PaperScraper():

    def __init__(self, **kwargs):
        """
        Constructs a new PaperScraper
        """

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(os.path.abspath(__file__).replace("/PaperScraper.py","")+"/drivers/chromedriver",
                                  chrome_options=options)
        if('driver_location' in kwargs):
            driver = webdriver.Chrome(
                kwargs['driver_location'],
                chrome_options=options)

        self.driver = driver



    def __import_all_scrapers(self):
        return [ScienceDirect(self.driver)]

    def print_scrapable_websites(self):
        for website_scraper in self.__import_all_scrapers():
            print(", ".join(website_scraper.website))


    """
    Return a JSON file containing a the full text and meta data of the paper located at 'url'.
    Returns None if 'url' cannot be scraped.
    
    """
    def extract_from_url(self, url):
        for website_scraper in self.__import_all_scrapers():
            if(website_scraper.is_correct_url(url)):
                return website_scraper.extract(url)
        return None
