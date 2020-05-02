from Bio import Entrez
import json
import re
from collections import Counter
import pandas as pd
from bs4 import BeautifulSoup as bs

email = 'shah7567@colorado.edu'


def search(query, retmax='20'):
    Entrez.email = email
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax=retmax,
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = email
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

def get_abstract(paper):
    try:
        return paper['MedlineCitation']['Article']['ArticleTitle'], \
    '\n'.join(paper['MedlineCitation']['Article']['Abstract']['AbstractText'])
    except:
        return None, None

def search_terms_in_title(title, search_terms):
    for term in search_terms:
        if term.lower() in title.lower():
            return True
    return False
    
def save_abstracts(search_terms, output_file_path, term_in_title=False, retmax=100000):
    id_list = []
    for term in search_terms:
        results = search(term, str(retmax))
        id_list.extend(results['IdList'])
    
    rows = []
    
    for i in range(0, len(id_list), 100):
        papers = fetch_details(id_list[i:i+100])
        for paper in papers['PubmedArticle']:
            title, abstract = get_abstract(paper)
            if title != None:
                if (not term_in_title) or search_terms_in_title(title, search_terms):
                    rows.append([str(title), bs(str(abstract)).text])
    columns=['Title', 'Abstract']
    df_final = pd.DataFrame(rows, columns=columns)
    df_final.to_csv(output_file_path, index=False)
    
# term = 'eczema'
# retmax = '100000'
# results = search(term, retmax)
# id_list = results['IdList']
# rows = []
# if len(id_list) > 0:
#     for i in range(0, len(id_list), 100):
#         papers = fetch_details(id_list[i:i+100])
#         for paper in papers['PubmedArticle']:
#             title, abstract = get_abstract(paper)
#             if title != None:
#                 rows.append([str(title), bs(str(abstract)).text])
#             # df.append({'Title':str(title), 'Abstract':str(abstract)}, ignore_index=True)
#             pass
# df_final = pd.DataFrame(rows, columns=columns)
# df_final.to_csv('ad_pm.csv', index=False)