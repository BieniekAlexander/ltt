# imports
import pymongo, logging
from bson.objectid import ObjectId

# constants
DATABASE = "lexicon"


class CollectionConnctor(object):
  """
  An interface that lets us connect to a document store 
  """
  def __init__(self, uri, database_name, collection_name):
    """
    Establish an initial connection to the document store
    """
    self.client = pymongo.MongoClient(uri)
    self.db = self.client.admin

    if self.db.command("serverStatus"):
      logging.info("Connected to mongodb and got server status")

    self.db = self.client[database_name]
    self.collection = self.db[collection_name]


  def get_document_mapping(self, query):
    """
    Wrapper for getting documents from datastore, given a [query]
    """
    assert isinstance(query, dict)
    results = list(self.collection.find(query))

    if len(results) > 1:
       # TODO make specific error type
      raise Exception(f"Found more than one result when trying to get a document, given a query - '{query}'")
    elif len(results) == 0:
      raise Exception(f"Found no results when trying to get a document, given a query - '{query}'")
    else:
      result = results[0]
      key = str(result.pop('_id'))
      value = result
      return (key, value)


  def get_document_mappings(self, query):
      """
      Get a dictionary containing the id: document mappings, given a query
      """
      assert isinstance(query, dict)
      result_set = self.collection.find(query)

      def get_dictionary_id_tuple(dictionary, key): # TODO rename tbh
        id = dictionary.pop(key)
        return (str(id), dictionary)

      results = list(result_set)
      mappings = dict(list(map(lambda x: get_dictionary_id_tuple(x, '_id'), results)))

      return mappings


  def push_document(self, document):
    """
    Insert a [document] and get the _id it gets mapped to
    """
    assert isinstance(document, dict)

    result = self.collection.insert_one(document)
    return result.inserted_id


  def push_documents(self, documents):
    """
    Insert a list of [lexemes] and get the _ids that they map to
    """
    # TODO what if some fail?
    assert all(isinstance(document, dict) for document in documents)
    results = self.collection.insert_many(documents)
    return list(map(lambda x: str(x), results.inserted_ids))
    

  def pop_document_mapping(self, query):
    """
    Pop a single document, given a query
    """
    assert isinstance(query, dict)
    _id, document = self.get_document_mapping(query)
    self.collection.delete_one({'_id': ObjectId(_id)})
    return (_id, document)


  def pop_document_mappings(self, query):
    """
    Pop documents, given a [query]

    https://stackoverflow.com/a/18567093
    """
    assert isinstance(query, dict)
    mappings = self.get_document_mappings(query)

    if not mappings: # TODO exception type
      raise Exception("Pop operation returned no entries")

    self.collection.delete_many(query)
    return mappings


# main
def main():
  db = CollectionConnctor("mongodb://localhost:27017/", 'lexicon', 'polish')
  print(list(db.collection.find({'lemma': 'z'})))


if __name__ == "__main__":
  main()

  