from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
"""An abstract wrapper for a scientific paper website scraper"""

class PaperSite(ABC):

    """
    Should pass through Selenium webdriver instance with your browser of preference
    """
    def __init__(self,driver):
        self.driver = driver


    def extract(self, url):
        """A method to handle the extraction of data """
        if (self.website not in url):
            raise ValueError("Not a %s article: %s" % (self.website, url))

        driver = self.driver
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        return {
            'title':self.get_title(soup),
            'authors': self.get_authors(soup),
            'keywords': self.get_keywords(soup),
            'abstract': self.get_abstract(soup),
            'body': self.get_body(soup),
            'doi':self.get_doi(soup),
            'pdf_url':self.get_pdf_url(soup)
        }


    @abstractmethod
    def get_authors(self, soup):
        """
            Returns a dict of authors structured as
                a1 : {
                    first_name : fname,
                    last_name : lname
                },
                a2 : {
                    first_name : fname,
                    last_name : lname
                }

            Notice, a1 should be first author.
        """
        pass


    @abstractmethod
    def get_body(self, soup):
        """
            Returns a dict of sections structured as
                section1 : {
                    p1 : contents,
                    p2 : contents,
                    ...
                    pn : contents
                },
                section2 : {
                    p1 : contents,
                    p2 : contents,
                    ...
                    pn : contents
                }

        """
        pass


    @abstractmethod
    def get_abstract(self,soup):
        """
            Returns the abstract of the paper
        """
        pass



    @abstractmethod
    def get_doi(self, soup):
        """
        Returns a string representation of paper DOI or 'NONE' if non-existant
        """
        pass


    @abstractmethod
    def get_title(self, soup):
        """
        Returns a string representation of paper title
        """
        pass


    @abstractmethod
    def get_pdf_url(self, soup):
        """
        Returns a string representation of url to PDF version of paper or 'NONE' if non-existant
        """
        pass


    @abstractmethod
    def get_keywords(self, soup):
        """
        Returns an array of keywords associated with a paper or 'NONE' if non-existant
        """
        pass

