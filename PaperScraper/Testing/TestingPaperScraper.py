from PaperScraper import PaperScraper
from pprint import pprint

ps = PaperScraper()

"""
Science Direct
https://www.sciencedirect.com/science/article/pii/S0144861713011806?via%3Dihub
https://www.sciencedirect.com/science/article/pii/S0041008X08003888?via%3Dihub
https://www.sciencedirect.com/science/article/pii/S0142961209006929?via%3Dihub


PMC
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3418173/


ACS:
https://pubs.acs.org/doi/10.1021/bm401141u

Wiley:
http://onlinelibrary.wiley.com/doi/10.1002/bit.24558/abstract;jsessionid=D467FB68F189881D513A8AA2368FBE34.f02t01


"""



#https://pubs.acs.org/doi/10.1021/nn4061012


json = ps.extract_from_url("http://linkinghub.elsevier.com/retrieve/pii/S1549-9634(10)00005-5")

pprint(json)