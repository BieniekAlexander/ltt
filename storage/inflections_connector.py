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


class InflectionsConnector(CollectionConnctor):
  """
  A [DocumentStoreConnector] used specifically for interacting with a language's inflection mapping collection
  """
  def __init__(self, uri, language):
    self.language = language.lower()
    super(InflectionsConnector, self).__init__(uri, DATABASE, language)
  
  
  def push_inflection_entry(self, lexeme_id: str, form: str, pos: str) -> str:
    """
    Add a new inflection to the datastore, represented by a [lexeme_id], [form], and [pos]
    """
    lexeme_id = ObjectId(lexeme_id)
    entry = {'lexeme_id': lexeme_id, 'form': form, 'pos': pos}
    return super(InflectionsConnector, self).push_document(entry)


  def push_inflection_entries(self, entries: list) -> list:
    """
    Add list of inflections to the datastore, each represented by a dictionary

    dictionaries must contain 'lexeme_id', 'form', and 'pos'
    """
    assert isinstance(entries, list)

    for entry in entries:
      assert isinstance(entry, dict)
      assert all(key in entry for key in ['lexeme_id', 'form', 'pos']), "Each inflection entry must contain a lexeme_id, a form, and a pos"
      assert isinstance(entry['form'], str)
      assert isinstance(entry['pos'], str)
      entry['lexeme_id'] = ObjectId(entry['lexeme_id'])

    return super(InflectionsConnector, self).push_documents(entries)


  def get_inflection_entry_mapping(self, lexeme_id: str = None, form: str = None, pos: str = None) -> dict:
    """
    Get inflection data and its _id, given the [lexeme_id], [form], and [pos]
    """
    if lexeme_id: lexeme_id = ObjectId(lexeme_id)
    query = generate_query(lexeme_id=lexeme_id, form=form, pos=pos)
    return super(InflectionsConnector, self).get_document_mapping(query)

  
  def get_inflection_entry_mappings(self, lexeme_ids: list = None, forms: list = None, poses: list = None) -> dict:
    """
    Get inflection data entries and their _ids, given the [lexeme_ids], [forms], and [poses]
    """
    if isinstance(lexeme_ids, list):
      lexeme_ids = list(map(ObjectId, lexeme_ids))
    elif lexeme_ids:
      lexeme_ids = ObjectId(lexeme_ids)

    query = generate_query(lexeme_id=lexeme_ids, form=forms, pos=poses)
    return super(InflectionsConnector, self).get_document_mappings(query)


  def pop_inflection_entry_mapping(self, lexeme_id: str = None, form: str = None, pos: str = None) -> dict:
    """
    Pop inflection data entry and its _id, given the [lexeme_id], [form], and [pos]
    """
    if lexeme_id: lexeme_id = ObjectId(lexeme_id)
    query = generate_query(lexeme_id=lexeme_id, form=form, pos=pos)
    return super(InflectionsConnector, self).pop_document_mapping(query)
  
  
  def pop_inflection_entry_mappings(self, lexeme_ids: list = None, forms: list = None, poses: list = None) -> dict:
    """
    Pop inflection data entries and their _ids, given the [lexeme_ids], [forms], and [poses]
    """
    if isinstance(lexeme_ids, list):
      lexeme_ids = list(map(ObjectId, lexeme_ids))
    elif lexeme_ids:
      lexeme_ids = ObjectId(lexeme_ids)

    query = generate_query(lexeme_id=lexeme_ids, form=forms, pos=poses)
    return super(InflectionsConnector, self).pop_document_mappings(query)
 

# main
def main():
  pass

if __name__ == "__main__":
  main()