
from websites.PaperSite import PaperSite
import re
from pprint import pprint
"""A scraper of a science direct articles"""


class ScienceDirect(PaperSite):

    def __init__(self,driver):
        self.driver = driver
        self.website = "sciencedirect.com"

    def get_authors(self, soup):
        authors_first = soup.find("div", {"class": "AuthorGroups"}).findAll("span", {"class": "given-name"})
        authors_last = soup.find("div", {"class": "AuthorGroups"}).findAll("span", {"class": "surname"})
        authors = {};

        for i in range(len(authors_first)):
            authors['a'+str(i+1)] = {'last_name':authors_last[i].contents[0], 'first_name':authors_first[i].contents[0]}

        return authors


    def get_body(self,soup):
        head_section = soup.find("div", {"class": "Body"}).find("div")

        [tag.decompose() for tag in head_section.findAll(["a","span", "figure"])]
        [tag.unwrap() for tag in head_section.findAll(["em","i","b","sub","sup"])]

        body = {}
        self._get_body_helper(head_section, body)
        return body



    def _get_body_helper(self, section, dict):
        """
        Every section has a title and either paragraphs or paragraphs and subsections.
        Recursively traverse these subsections and add to dict.
        """
        section_title = section.find(["h1", "h2", "h3", "h4", "h5"]).getText()
        paragraphs = section.findAll("p", recursive=False)
        subsections = section.findAll("section", recursive=False)


        if(not subsections): #no subsections exist
            if(paragraphs):
                dict[section_title] = {}
                for i in range(len(paragraphs)):
                    paragraph_text = paragraphs[i].getText()
                    paragraph_text = paragraph_text.replace("()", "") # a slight clean up from link removal
                    dict[section_title]['p' + str(i)] = paragraph_text
        else:
            for section in subsections:
                self._get_body_helper(section, dict)

    def get_doi(self,soup):
        return soup.find("meta", {"name":"citation_doi"})['content'] or "NONE"

    def get_title(self,soup):
        return soup.find("meta", {"name": "citation_title"})['content']

    def get_pdf_url(self, soup):
        return soup.find("meta", {"name": "citation_pdf_url"})['content'] or "NONE"

    def get_abstract(self,soup):
        return soup.find("div", {"class": "abstract author"}).find("p").contents[0]

    def get_keywords(self, soup):
        return [x.contents[0] for x in soup.find("div", {"class": "keywords-section"}).findAll("span")] or "NONE"

