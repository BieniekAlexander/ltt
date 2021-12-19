# imports
import sys, os, json
from bson.objectid import ObjectId


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.collection_connector import CollectionConnctor
from storage.datastore_utils import generate_query
from model.lexeme import LexemeEncoder, Lexeme
from model.part_of_speech import PartOfSpeech
from model.polish.pos.preposition import Preposition
from model import model_class_map

# constants
DATABASE = "lexicon"


class LexiconConnector(CollectionConnctor):
  """
  A [DocumentStoreConnector] used specifically for interacting with a language's lexicon
  """
  def __init__(self, uri, language):
    super(LexiconConnector, self).__init__(uri, DATABASE, language)
    self.language = language
  
  
  def get_lexeme_dictionary_mapping(self, lemma=None, _id=None):
    """
    Get an (id, lexeme dictionary) mapping, given the [lemma] form or the mongodb [_id]
    """
    assert (lemma and not _id) or (not lemma and _id), "provide only a lemma or an _id to find your lexeme"
    query = generate_query(lemma=lemma, _id=_id)
    return super(LexiconConnector, self).get_document_mapping(query)


  def get_lexeme_mapping(self, lemma=None, _id=None):
    """
    Get an (id, lexeme) mapping, given the [lemma] form or the [_id]
    """
    key, lexeme_dictionary = self.get_lexeme_dictionary_mapping(lemma=lemma, _id=_id)
    cls = model_class_map[self.language.upper()][lexeme_dictionary['pos']]
    lexeme = cls(**lexeme_dictionary)
    return (key, lexeme)


  def get_lexeme_dictionary_mappings(self, lemmas=None, _ids=None):
      """
      Get a dictionary containing the id: lexeme_dictionary mappings, given a list of [lemmas] or [_ids]
      """    
      assert (lemmas and not _ids) or (not _ids and lemmas), "provide only a list of lemmas or a list of _ids"
      query = generate_query(lemma=lemmas, _id=_ids)
      return super(LexiconConnector, self).get_document_mappings(query)

  
  def get_lexeme_mappings(self, lemmas=None, _ids=None):
    """
    Get a dictionary containing the id: lexeme mappings, given a list of [lemmas] or [_ids]
    """
    dictionary_mappings = self.get_lexeme_dictionary_mappings(lemmas=lemmas, _ids=_ids)
    lexeme_mappings = {}

    for key, lexeme_dictionary in dictionary_mappings.items():
      cls = model_class_map[self.language.upper()][lexeme_dictionary['pos']]
      lexeme = cls(**lexeme_dictionary)
      lexeme_mappings[key] = lexeme

    return lexeme_mappings

  
  def cast_lexeme_dictionary(self, lexeme):
    """
    Cast a [lexeme] to a dictionary type if it's not already a dictionary
    """
    if isinstance(lexeme, dict):
      return lexeme
    elif isinstance(lexeme, Lexeme):
      return lexeme.to_json_dictionary()
    else:
      # TODO make exception type
      raise Exception(f"Unexpected type when inserting lexeme into collection - {type(lexeme)}")


  def push_lexeme(self, lexeme):
    """
    Insert a [lexeme_dict] and get the _id it gets mapped to
    """
    lexeme_dict = self.cast_lexeme_dictionary(lexeme)
    return super(LexiconConnector, self).push_document(lexeme_dict)


  def push_lexemes(self, lexemes):
    """
    Insert a list of [lexemes] and get the _ids that they map to
    """
    # TODO what if some fail?
    lexeme_dicts = list(map(lambda x: self.cast_lexeme_dictionary(x), lexemes))
    return super(LexiconConnector, self).push_documents(lexeme_dicts)
    

  def pop_lexeme_dictionary_mapping(self, lemma=None, _id=None):
    """
    Pop a lexeme dictionary, given the [lemma] or [_id]
    """
    assert lemma or _id, "provide a lemma or an _id to find your lexeme"
    query = generate_query(lemma=lemma, _id=_id)
    return super(LexiconConnector, self).pop_document_mapping(query)


  def pop_lexeme_mapping(self, lemma=None, _id=None):
    """
    Pop a lexeme, given the [lemma] or [_id]
    """
    _id, lexeme_dict = self.pop_lexeme_dictionary_mapping(lemma, _id)
    cls = model_class_map[self.language.upper()][lexeme_dict['pos']]
    lexeme = cls(**lexeme_dict)
    return (_id, lexeme)


  def pop_lexeme_dictionary_mappings(self, lemmas=None, _ids=None):
    """
    Pop [Lexeme], given the [lemma] or [_id]

    https://stackoverflow.com/a/18567093
    """
    assert (lemmas and not _ids) or (not _ids and lemmas), "provide only a list of lemmas or a list of _ids"
    mappings = self.get_lexeme_dictionary_mappings(lemmas=lemmas, _ids=_ids)
    query = generate_query(lemma=lemmas, _id=_ids)   
    return super(LexiconConnector, self).pop_document_mappings(query)


  def pop_lexeme_mappings(self, lemmas=None, _ids=None):
    """
    Pop [Lexeme], given the [lemma] or [_id]

    https://stackoverflow.com/a/18567093
    """
    lexeme_dictionary_mappings = self.pop_lexeme_dictionary_mappings(lemmas=lemmas, _ids=_ids)
    lexeme_mappings = {}
    
    for key in lexeme_dictionary_mappings:
      lexeme_dict = lexeme_dictionary_mappings[key]
      cls = model_class_map[self.language.upper()][lexeme_dict['pos']]
      lexeme = cls(**lexeme_dict)
      lexeme_mappings[key] = lexeme

    return lexeme_mappings


# main
def main():
  polish_lexicon = LexiconConnector("mongodb://localhost:27017/", 'polish')
  lemmas = ['aaa', 'bbb', 'ccc']
  lexemes = [Preposition(l, PartOfSpeech.PREPOSITION, [], []) for l in lemmas]
  # result = polish_lexicon.push_lexemes(lexemes)

  result = polish_lexicon.pop_lexeme_mappings(lemmas=lemmas)
  print(result)

  # results = polish_lexicon.get_lexeme_dictionary_mappings(['pod', 'za'])
  # print(list(results))

if __name__ == "__main__":
  main()