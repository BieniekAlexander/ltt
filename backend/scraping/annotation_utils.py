#%% imports
import os, sys, re, logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.language_datastore import LanguageDatastore
from storage.vocabulary_connector import VocabularyConnector
from scraping.wiktionary_extract_lexeme_utils import extract_lexeme
from scraping.wiktionary_crawl_utils import get_lexeme_page_soup

#%% utils
def annotate_text(text: str, language_datastore: LanguageDatastore, vocabulary_connector: VocabularyConnector = None, discovery_mode: bool = False):
  """
  Take in a piece of text and annotate it using data from the given language_datastore

  If [discovery_mode]==[True], unknown terms will be added to the [language_datastore]
  """
  assert isinstance(text, str)

  terms = list(map(lambda x: x.lower(), re.findall(r'\w+', text)))
  language = language_datastore.language
  annotations = []

  for i, term in enumerate(terms):
    # how are we identifying the most probable lexeme - especially if we don't know the POS?
    potential_lexeme_dictionary_mappings = language_datastore.get_lexemes_from_form(form=term)
    annotation = {'term': term}

    # get lexeme from lexicon
    if potential_lexeme_dictionary_mappings:
      entry = potential_lexeme_dictionary_mappings[0]
      print(entry)
      annotation['lexeme_id'] = str(entry.pop('_id'))
      annotation['lexeme'] = entry
    else:
      if discovery_mode:
        try:
          term_soup, lemma, pos = get_lexeme_page_soup(term, None, language)
          annotation['lexeme'] = extract_lexeme(term_soup, lemma, pos, language)
          annotation['lexeme_id'] = language_datastore.add_lexeme(annotation['lexeme'])
        except:
          logging.error(f"Tried & failed to scrape the {i}th term - {term}")
      else:
        logging.warning(f"Failed to annotate the {i}th term - {term} (discovery disabled)")

    if 'lexeme' in annotation:
      # try to get lexeme from a user's vocabulary
      if vocabulary_connector:
        vocabulary_id, entry = vocabulary_connector.get_vocabulary_entry(annotation['lexeme_id'])
        
        if vocabulary_id:
          annotation['vocabulary_id'] = vocabulary_id
          annotation['rating'] = entry['rating']

    annotations.append(annotation)

  return annotations