#%% imports
import sys, os, requests, time, json, re, logging
from bs4 import BeautifulSoup
import pymongo

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scraping.wiktionary_scrape_summary_utils import wiktionary_get_all_lang_pos_lemmas
from scraping.wiktionary_extract_lexeme_utils import extract_lexeme
from model.lexeme import LexemeEncoder
from scraping.wiktionary_crawl_utils import get_lexeme_page_soup

MONGODB_URL = "mongodb://localhost:27017/"
DATABASE = "vocabulary"
COLLECTION = "polish"
PATH_TO_TEXT = "/home/alex/projects/ltt/run/data/polish/taniec.txt"


#%% setup
# set up mongodb connection 
# TODO uncomment
# client = pymongo.MongoClient(MONGODB_URL)
# mongodb_collection_polish = client[DATABASE][COLLECTION]

language = "Polish"
text = open(PATH_TO_TEXT, "r").read()
forms = list(map(lambda x: x.lower(), re.findall(r'\w+', text)))


# %%
for form in forms:
  try:
    term_soup, lemma, pos = get_lexeme_page_soup(form, None, language)
    lexeme = extract_lexeme(term_soup, lemma, pos, language)

    with open(f"data/polish/{pos.lower()}_{lexeme.lemma.replace(' ', '_')}.json", 'w') as f:
      json_dict = lexeme.to_json_dictionary()
      
      json_str = json.dumps(lexeme, cls=LexemeEncoder)
      f.write(json_str)
      # mongodb_collection_polish.insert_one(json_dict)

    print(f"saved {form} -> {lemma}")
  
  except Exception as e:
    print(f"failed to collect lexeme for {form} - {e}")