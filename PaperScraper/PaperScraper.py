from aggregators.PubMedAggregator import PubMedAggregator
from websites.ScienceDirect import ScienceDirect
from websites.ACS import ACS
from selenium import webdriver
import os

##temp
from pprint import pprint
##
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def __import_all_scrapers(self):
        return [ScienceDirect(self.driver), ACS(self.driver)]

    def print_scrapable_websites(self):
        for website_scraper in self.__import_all_scrapers():
            print("\n".join(website_scraper.website))

    def is_scrapable(self,url):
        """
        Checks if a given url is scrapable by PaperScraper

        :param url: a url containing a full text that needs scrapping
        :return: the Scraper that implements PaperSite that can scrape url or None
        """

        for website_scraper in self.__import_all_scrapers():
            if(website_scraper.is_correct_url(url)):
                return website_scraper
        return None

    def extract_from_url(self, url):
        """
           Return a JSON file containing a the full text and meta data of the paper located at 'url'.
           Returns None if 'url' cannot be scraped.
           """
        for website_scraper in self.__import_all_scrapers():
            if(website_scraper.is_correct_url(url)):
                return website_scraper.extract(url)
        return None

    def extract_from_pmid(self,pmid):
        pm = PubMedAggregator(self.driver)
        all_sites = pm.extract(pmid)
        for url in [all_sites.get(key)['href'] for key in all_sites.keys()]:
            website_scraper = self.is_scrapable(url)
            if website_scraper is not None:
                return self.extract_from_url(url)

        return None

    def get_sites_from_pmid(self, pmid):
        pm = PubMedAggregator(self.driver)
        all_sites = pm.extract(pmid, follow_link=True)
        return [all_sites.get(key)['href'] for key in all_sites.keys()]