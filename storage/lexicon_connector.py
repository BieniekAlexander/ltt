# imports
import sys, os

from bson.objectid import ObjectId

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.collection_connector import CollectionConnctor
from storage.datastore_utils import cast_enum_to_str, generate_query
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
    self.language = language.lower()
    super(LexiconConnector, self).__init__(uri, DATABASE, language)
  
  
  def get_lexeme_dictionary_mapping(self, lemma=None, pos=None, _id=None):
    """
    Get (id, [Lexeme] [dict]) mapping, given either an [_id] or a [lemma] and/or [pos]
    """
    # preprocess args
    if _id:
      assert not lemma and not pos, "supply either _ids, or lemmas and/or poses"
      _id = ObjectId(_id)
    else:
      assert pos or lemma, "supply either _ids, or lemmas and/or poses"
      if pos: pos = cast_enum_to_str(pos)

    query = generate_query(lemma=lemma, _id=_id, pos=pos)
    return super(LexiconConnector, self).get_document_mapping(query)


  def get_lexeme_mapping(self, lemma=None, pos=None, _id=None):
    """
    Get (id, [Lexeme]) mapping, given either an [_id] or a [lemma] and/or [pos]
    """
    key, lexeme_dictionary = self.get_lexeme_dictionary_mapping(lemma=lemma, pos=pos, _id=_id)
    cls = model_class_map[self.language.upper()][lexeme_dictionary['pos']]
    print(lexeme_dictionary)
    print(cls)
    lexeme = cls(**lexeme_dictionary)
    return (key, lexeme)


  def get_lexeme_dictionary_mappings(self, lemmas=None, poses=None, _ids=None):
    """
    Get (id, [Lexeme] [dict]) mappings, given either [_ids], or [lemmas] and/or [poses]
    """
    # preprocess args
    if _ids:
      assert not lemmas and not poses, "supply either _ids, or lemmas and/or poses"
      if isinstance(_ids, list):
        _ids = list(map(ObjectId, _ids))
      else:
        _ids = ObjectId(_ids)
    else:
      assert lemmas or poses, "supply either _ids, or lemmas and/or poses"
      if isinstance(poses, list):
        poses = list(map(cast_enum_to_str, poses))
      elif poses:
        poses = cast_enum_to_str(poses)

    query = generate_query(lemma=lemmas, _id=_ids, pos=poses)
    return super(LexiconConnector, self).get_document_mappings(query)

  
  def get_lexeme_mappings(self, lemmas=None, poses=None, _ids=None):
    """
    Get (id, [Lexeme] [dict]) mappings, given either [_ids], or [lemmas] and/or [poses]
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
    Insert a [Lexeme] and get the _id it gets mapped to
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
    

  def pop_lexeme_dictionary_mapping(self, lemma=None, pos=None, _id=None):
    """
    Pop a [Lexeme] dictionary, given either an [_id] or a [lemma] and/or [pos]
    """
    # preprocess args
    if _id:
      assert not lemma and not pos, "supply either _ids, or lemmas and/or poses"
      _id = ObjectId(_id)
    else:
      assert pos or lemma, "supply either _ids, or lemmas and/or poses"
      if pos: pos = cast_enum_to_str(pos)

    query = generate_query(lemma=lemma, _id=_id, pos=pos)
    return super(LexiconConnector, self).pop_document_mapping(query)


  def pop_lexeme_mapping(self, lemma=None, pos=None, _id=None):
    """
    Pop a lexeme, given the [lemma] or [_id]
    """
    _id, lexeme_dict = self.pop_lexeme_dictionary_mapping(lemma, pos, _id)
    cls = model_class_map[self.language.upper()][lexeme_dict['pos']]
    lexeme = cls(**lexeme_dict)
    return (_id, lexeme)


  def pop_lexeme_dictionary_mappings(self, lemmas=None, poses=None, _ids=None):
    """
    Pop [Lexeme] dictionaries, given either [_ids], or [lemmas] and/or [poses]

    https://stackoverflow.com/a/18567093
    """
    # preprocess args
    if _ids:
      assert not lemmas and not poses, "supply either _ids, or lemmas and/or poses"
      if isinstance(_ids, list):
        _ids = list(map(ObjectId, _ids))
      else:
        _ids = ObjectId(_ids)
    else:
      assert lemmas or poses, "supply either _ids, or lemmas and/or poses"
      if isinstance(poses, list):
        poses = list(map(cast_enum_to_str, poses))
      elif poses:
        poses = cast_enum_to_str(poses)

    mappings = self.get_lexeme_dictionary_mappings(lemmas=lemmas, poses=poses, _ids=_ids)
    query = generate_query(lemma=lemmas, _id=_ids)   
    return super(LexiconConnector, self).pop_document_mappings(query)


  def pop_lexeme_mappings(self, lemmas=None, poses=None, _ids=None):
    """
    Pop [Lexeme]s, given either [_ids], or [lemmas] and/or [poses]

    https://stackoverflow.com/a/18567093
    """
    lexeme_dictionary_mappings = self.pop_lexeme_dictionary_mappings(lemmas=lemmas, poses=poses, _ids=_ids)
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