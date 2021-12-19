# imports
import sys, os, json
from bson.objectid import ObjectId

from storage.datastore_utils import generate_query


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.collection_connector import CollectionConnctor
from model.lexeme import LexemeEncoder, Lexeme
from model.part_of_speech import PartOfSpeech
from model.polish.pos.preposition import Preposition
from model import model_class_map

# constants
DATABASE = "inflections"


class InflectionConnector(CollectionConnctor):
  """
  A [DocumentStoreConnector] used specifically for interacting with a language's inflection mapping collection
  """
  def __init__(self, uri, language):
    super(InflectionConnector, self).__init__(uri, DATABASE, language)
    self.language = language
  
  
  def push_inflection_entry(self, entry: dict = None, lemma: str = None, form: str = None, pos: str = None) -> str:
    """
    Add a new inflection to the datastore, represented by an [entry] dict or a [lemma], [form], and [pos]
    """
    assert (entry and not lemma and not form and not pos) or (not entry and lemma and form and pos), "Only supply either an entry dict, or the keys of an entry"

    if lemma and form and pos:
      entry = {'lemma': lemma, 'form': form, 'pos': pos}

    if any(key not in entry for key in ['lemma', 'form', 'pos']):
      # TODO more specific exception
      raise Exception(f"missing lemma, form, or pos for this entry - {entry}")

    return super(InflectionConnector, self).push_document(entry)


  def push_inflection_entries(self, entries: list) -> list:
    """
    Add list of inflections to the datastore, each represented by a dictionary

    dictionaries must contain 'lemma', 'form', and 'pos'
    """
    assert isinstance(entries, list)

    for entry in entries:
      assert isinstance(entry, dict)
      assert all(key in entry for key in ['lemma', 'form', 'pos']), "Each inflection entry must contain a lemma, a form, and a pos"

    return super(InflectionConnector, self).push_documents(entries)


  def get_inflection_entry_mapping(self, lemma: str = None, form: str = None, pos: str = None) -> dict:
    """
    Get inflection data and its _id, given the [lemma], [form], and [pos]
    """
    query = generate_query(lemma=lemma, form=form, pos=pos)
    return super(InflectionConnector, self).get_document_mapping(query)

  
  def get_inflection_entry_mappings(self, lemmas: list = None, forms: list = None, poses: list = None) -> dict:
    """
    Get inflection data entries and their _ids, given the [lemmas], [forms], and [poses]
    """
    query = generate_query(lemma=lemmas, form=forms, pos=poses)
    return super(InflectionConnector, self).get_document_mappings(query)


  def pop_inflection_entry_mapping(self, lemma: str = None, form: str = None, pos: str = None) -> dict:
    """
    Pop inflection data entry and its _id, given the [lemma], [form], and [pos]
    """
    query = generate_query(lemma=lemma, form=form, pos=pos)
    return super(InflectionConnector, self).pop_document_mapping(query)
  
  
  def pop_inflection_entry_mappings(self, lemmas: list = None, forms: list = None, poses: list = None) -> dict:
    """
    Pop inflection data entries and their _ids, given the [lemmas], [forms], and [poses]
    """
    query = generate_query(lemma=lemmas, form=forms, pos=poses)
    return super(InflectionConnector, self).pop_document_mappings(query)
 

# main
def main():
  pass

if __name__ == "__main__":
  main()