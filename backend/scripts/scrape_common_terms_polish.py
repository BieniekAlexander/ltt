'''
This script collects information on the 2000 most common polish words,
collected from this article: https://www.101languages.net/polish/most-common-polish-words/
duolingo terms from here: https://www.duolingo.com/words
'''
#%% imports
import os, logging
import pandas as pd
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient


from scraping.wiktionary_spider import WiktionarySpider
from scraping.scraping_errors import ScrapingError
from storage.language_datastore import LanguageDatastore

MONGODB_URL = "mongodb://localhost:27017/"
PATH_TO_CSV = f"{os.getcwd()}/data/polish/duolingo_vocab.csv"
os.makedirs('logs/2k', exist_ok=True)


# %% setup
# set up mongodb connection
language = "polish"
polish_terms_df = pd.read_csv(PATH_TO_CSV)
polish_terms = list(polish_terms_df['Polish'])

ds_client = MongoClient(MONGODB_URL)
language_datastore = LanguageDatastore(ds_client, language)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# %% helper functions
def get_error_summary(term: str, exception: Exception, spider: WiktionarySpider, num_urls: int = 3) -> str:
  # TODO maybe retrieve error summary info (i.e. ScrapingError query information) from the object itself, rather than conditionally pulling things out by name
  assert num_urls > 0

  urls_to_show = spider.steps[-num_urls:]
  url_str = '\n'.join(urls_to_show)
  query_str = f"query: {exception.query_args}\n" if issubclass(type(exception), ScrapingError) else ""

  return ("Error Summary\n"
  f"term: {term}\n"
  f"{query_str}"
  f"exception: {type(exception).__name__}\n"
  f"message: {exception}\n"
  "urls:\n"
  f"{url_str}")


# %%
for term in polish_terms:  
  term = term.lower() # lowercase the term for reading from database and scraping from wiktionary - TODO what to do about proper nouns?
  potential_lexeme_dictionary_mappings = language_datastore.get_lexemes_from_form(form=term.lower())

  # get lexeme from lexicon
  if potential_lexeme_dictionary_mappings:
    entry = potential_lexeme_dictionary_mappings[0]
    lemma = entry['lemma']
    logger.debug(f"Found lemma {lemma} in datastore (found using term {term})")
  else:
    try:
      spider = WiktionarySpider()
      lexemes = spider.query_lexemes(term, language)

      for lexeme in lexemes:
        try:
          lexeme_id = language_datastore.add_lexeme(lexeme)
          logger.info(f"Saved {lexeme.lemma, lexeme.pos.value} to datastore (found using term {term})")
        except DuplicateKeyError as e:
          pass
      
    except Exception as e:
      logger.error(f"Tried & failed to scrape the term {term} - {type(e).__name__}: {e}")

      with open(f'logs/2k/{term}.log', 'w') as f:
        f.write(get_error_summary(term, e, spider, 3))
