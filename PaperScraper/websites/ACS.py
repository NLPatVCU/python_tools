from .PaperSite import PaperSite
"""A scraper for American Chemical Society (ACS) articles"""


class ACS(PaperSite):

    def __init__(self, driver):
        self.driver = driver
        self.website = ["pubs.acs.org"]

    def get_authors(self, soup):
        author_links = soup.find("div", id="articleMeta").findAll("a", id="authors")
        authors = {};

        for i in range(len(author_links)):
            authors['a'+str(i+1)] = {'last_name':author_links[i].contents[0].split(" ")[-1], 'first_name':author_links[i].contents[0].split(" ")[0]}

        return authors

    def get_abstract(self,soup):
        return soup.find("p", {'class':'articleBody_abstractText'}).getText()

    def get_body(self, soup):
        pass
        #TODO Need Access

    def get_doi(self, soup):
        doi_block = soup.find("div", id="doi")
        doi_block.next_element.extract()
        return doi_block.getText()

    def get_keywords(self, soup):
        pass
        #TODO  Need Access

    def get_pdf_url(self, soup):
        return "https://pubs.acs.org" + soup.find("ul", {"class": "publicationFormatList icons"}).findAll("li")[0].find("a")['href']

    def get_title(self, soup):
        return soup.find("span", {"class": "hlFld-Title"}).getText()
