#%% imports
import sys, os, requests, time, json
from bs4 import BeautifulSoup
import pymongo

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from scraping.wiktionary_scrape_summary_utils import wiktionary_get_all_lang_pos_lemmas
from scraping.wiktionary_extract_lexeme_utils import extract_lexeme
from model.lexeme import LexemeEncoder

MONGODB_URL = "mongodb://localhost:27017/"
DATABASE = "vocabulary"
COLLECTION = "polish"


#%% main
def main():
  # set up mongodb connection
  client = pymongo.MongoClient(MONGODB_URL)
  mongodb_collection_polish = client[DATABASE][COLLECTION]

  summary_url = 'https://en.wiktionary.org/wiki/Category:Polish_prepositions'
  page = requests.get(summary_url)
  soup = BeautifulSoup(page.content, "html.parser")
  lemmas = wiktionary_get_all_lang_pos_lemmas(soup)

  for lemma in lemmas:
    time.sleep(3)
    term_url = f'https://en.wiktionary.org/wiki/{lemma}'
    page = requests.get(term_url)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
      lexeme = extract_lexeme(soup, lemma, 'preposition', 'polish')
      with open(f"data/polish/preposition_{lexeme.lemma.replace(' ', '_')}.json", 'w') as f:
        json_dict = lexeme.to_json_dictionary()
        mongodb_collection_polish.insert_one(json_dict)
        # json_str = json.dumps(lexeme, cls=LexemeEncoder)
        # f.write(json_str)
        
      print("saved lexeme")
    except Exception as e:
      print(e)


if __name__ == '__main__':
  main()