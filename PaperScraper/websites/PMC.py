from websites.PaperSite import PaperSite
from collections import OrderedDict
import re
"""A scraper for PMC articles"""

class PMC(PaperSite):

    def __init__(self,driver):
        self.driver = driver
        self.website = ["ncbi.nlm.nih.gov"]

    def get_authors(self, soup):
        authors = OrderedDict()
        author_links = soup.find("div", {"class": "contrib-group fm-author"}).findAll("a")
        for i in range(len(author_links)):
            authors['a'+str(i+1)] = {'last_name': author_links[i].contents[0].split(" ")[-1],
             'first_name': author_links[i].contents[0].split(" ")[0]}
        return authors

    def get_abstract(self,soup):
        abstract = soup.find("p", {"class": "p p-first-last"})
        return abstract.text
        #abstract = soup.find("div", id=lambda x: x and x.startswith('__abstract'))
        # print(abstract)
        # print(soup.find("p", id="__p1"))
        # [tag.unwrap() for tag in abstract.findAll(["em", "i", "b", "sub", "sup"])]
        # return abstract.find("p").contents[0]

    # In the terminal some characters aren't printed correctly, but they show up correctly when printed to
    # a text file.
    def get_body(self, soup):
        
        # Called on each section to get rid of table and figure content as well as remove links
        def clean_section(section):
            [tag.decompose() for tag in section.findAll(["a", "span", "figure"])]
            [div.decompose() for div in section.findAll("div", {"id": re.compile("f[0-9]-ijn(.*)")})]
            [div.decompose() for div in section.findAll("div", {"id": re.compile("t[0-9]-ijn(.*)")})]

        # Called on each paragraph to clean up the aftermath of link removal
        def clean_paragraph(paragraph):
            paragraph = paragraph.replace("()", "")
            paragraph = paragraph.replace(", )", ")")
            paragraph = paragraph.replace(" - ", "")
            paragraph = paragraph.replace(".,", ".")
            paragraph = paragraph.replace(",,", ",")
            return paragraph

        sections = OrderedDict()
        sections_markup = soup.findAll("div", {"class": "tsec sec", "id": re.compile("__sec(.*)")})

        for section_markup in sections_markup:
            paragraphs = OrderedDict()

            clean_section(section_markup)

            section_paragraphs = section_markup.findAll("p")

            for i in range(len(section_paragraphs)):
                paragraph_text = section_paragraphs[i].getText()
                paragraph_text = clean_paragraph(paragraph_text)
                paragraphs['p'+str(i+1)] = paragraph_text

            sections[section_markup.h2.getText()] = paragraphs

        return sections


    def get_doi(self, soup):
        return soup.find("span", {"class": "doi"}).find("a").getText()

    def get_keywords(self, soup):
        keywords =  soup.find("span", {"class": "kwd-text"})
        [tag.unwrap() for tag in keywords.findAll(["em", "i", "b", "sub", "sup"])]
        return keywords.getText().split(", ")

    def get_pdf_url(self, soup):
        return "https://www.ncbi.nlm.nih.gov/"+soup.find("div", {"class": "format-menu"}).findAll("li")[3].find("a")['href']

    def get_title(self, soup):
        return soup.find("h1", {"class": "content-title"}).getText()
