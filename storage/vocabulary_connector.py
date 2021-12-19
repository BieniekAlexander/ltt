# imports
import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.collection_connector import CollectionConnctor
from model.lexeme import LexemeDecoder, LexemeEncoder


# constants
DATABASE = "vocabulary"


class VocabularyConnector(CollectionConnctor):
  """
  A [DocumentStoreConnector] used specifically for interacting with a user's vocabulary
  """
  def __init__(self, uri, language):
    super(VocabularyConnector, self).__init__(uri, DATABASE, language)
    self.language = language
      
  
  def get_lexeme_dict(self, lemma):
    """
    Get a lexeme dictionary, given the [lemma] form
    """
    print(self.collection.name)
    results = list(self.collection.find({'lemma': lemma}))
    print(results)
    
    if len(results) > 1:
       # TODO make specific error type
      raise Exception(f"Found more than one result when trying to get a lemma from the {self.language} lexicon - '{lemma}'")
    elif len(results) == 0:
      raise Exception(f"Found no results when trying to get a lemma from the {self.language} lexicon - '{lemma}'")
    else:
      return results[0]


  def get_lexeme(self, lemma):
    """
    Get a lexeme, given the [lemma] form
    """
    lexeme_dict = self.get_lexeme_dict
    return json.load()


# main
def main():
  polish_lexicon = VocabularyConnector("mongodb://localhost:27017/", 'polish')
  lexeme_dict = polish_lexicon.get_lexeme_dict('zza')
  print(json.dumps(lexeme_dict, cls=LexemeEncoder))


if __name__ == "__main__":
  main()

  