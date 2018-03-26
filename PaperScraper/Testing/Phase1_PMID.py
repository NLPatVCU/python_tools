from PaperScraper import PaperScraper
from pprint import pprint
pmids = """25355699
9333048
9303390
24953566
12006516
16258082
7505268
22080439
22864522
24965808
25739672
18242722
23358650
11709329
21986846
17308894
21833442
25304209
25403217
20876255
9669400
10942366
8683227
7687326
26847057
20305636
25049380
18056191
23564374
19575282
19559353
22723563
9521260
9916886"""
ps = PaperScraper()

#pprint(ps.extract_from_url("https://www.sciencedirect.com/science/article/pii/S0144861713011806?via%3Dihub"))

for pmid in pmids.split("\n"):
    print(pmid)
    try:
        json_paper = ps.extract_from_pmid(pmid)
        if json_paper is not None:
            pprint(json_paper)
        else:
            print("Could not extract paper")
    except IOError as error:
        print(error)