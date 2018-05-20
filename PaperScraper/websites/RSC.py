from .PaperSite import PaperSite
from collections import OrderedDict
import re
import unicodedata
"""A scraper for The Royal Society of Chemistry (RSC) articles"""


class RCS(PaperSite):

    def __init__(self, driver):
        self.driver = driver
        self.website = ["pubs.rsc.org"]

    def get_authors(self, soup):

        authors = OrderedDict()
        author_tags = soup.findAll("meta", {"name": "citation_author"})
        regex = re.compile("\w\. ") # Regex to see if the author has a middle initial

        for i in range(len(author_tags)):
            author_name = unicodedata.normalize("NFKD", author_tags[i]['content'])

            # If there is a middle initial, split the middle initial into the first name category
            if regex.search(author_name):
                authors['a'+str(i+1)] = {'last_name': author_name.split(" ")[-1],
                    'first_name': " ".join(author_name.split(" ")[0:2])}
            else:
                authors['a'+str(i+1)] = {'last_name': author_name.split(" ")[-1],
                    'first_name': author_name.split(" ")[0]}

        return authors


    def get_abstract(self, soup):
        return soup.find("p", {'class': 'abstract'}).getText()

    def get_body(self, soup):

        # Called on each paragraph to clean up the aftermath of link removal
        def clean_paragraph(paragraph):
            paragraph = paragraph.replace("()", "")
            paragraph = paragraph.replace(", )", ")")
            paragraph = paragraph.replace(" - ", "")
            paragraph = paragraph.replace(".,", ".")
            paragraph = paragraph.replace(",,", ",")
            return paragraph

        sections = OrderedDict()

        # If there are sections iterate through the webpage and add them to the OrderedDict
        if (soup.find("h2") and soup.find("h2").getText() != "Notes and references"):
            for sibling in soup.find("p", {'class': 'abstract'}).next_siblings:
                if sibling.name == "h2":
                    # Stop at these sections because no relevant content
                    if (sibling.getText() == "Notes and references" or sibling.getText() == "Acknowledgements"):
                        break
                    paragraphs = OrderedDict()
                    counter = 1
                    print(sibling.getText())
                    for tag in sibling.next_siblings:
                        if (tag.name == "p" or tag.name == "span"):
                            [reference.decompose() for reference in tag.findAll(["a", "sup"])]
                            paragraph = clean_paragraph(tag.getText())
                            paragraphs['p'+str(counter)] = paragraph
                            counter += 1
                        if (tag.name == "h2"):
                            break
                    sections[sibling.getText()] = paragraphs
        # There are no sections so just return all relevant text under a "no_section" heading
        else:
            paragraphs = OrderedDict()
            counter = 1
            for sibling in soup.find("p", {'class': 'abstract'}).next_siblings:
                if (sibling.name == "p" or sibling.name == "span"):
                    # Stop at these sections because no relevant content.
                    if (sibling.getText() == "Notes and references" or sibling.getText() == "Acknowledgements"):
                        break
                    [tag.decompose() for tag in sibling.findAll(["a", "sup"])]
                    paragraph = clean_paragraph(sibling.getText())
                    paragraphs['p'+str(counter)] = paragraph
                    counter += 1

            sections["no_section"] = paragraphs

        return sections




    def get_doi(self, soup):
        return soup.find("meta", {"name": "citation_doi"})['content']

    """ Used to get the keywords from the article

        There are no keywords provided for RSC Articles. Still looking for equivalent.
        """
    def get_keywords(self, soup):
        pass

    def get_pdf_url(self, soup):
        return soup.find('a', {"title": "Link to PDF version"})['href']

    def get_title(self, soup):
        return soup.find("meta", {"name": "citation_title"})['content']
