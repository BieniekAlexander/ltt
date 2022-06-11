# imports
import queue
import pymongo, logging, os, sys
from bson.objectid import ObjectId
from pymongo import MongoClient


class CollectionConnector(object):
  """
  An interface that lets us connect to a document store 
  """
  def __init__(self, datastore_client: MongoClient, database_name: str, collection_name: str):
    """
    Establish an initial connection to the document store
    """
    self.collection = datastore_client[database_name][collection_name]


  def get_document(self, query: dict) -> dict:
    """
    Wrapper for getting documents from datastore, given a [query]
    """
    assert isinstance(query, dict)
    results = list(self.collection.find(query))

    if len(results) > 1:
       # TODO make specific error type
      raise Exception(f"Found more than one result when trying to get a document, given a query - '{query}'")
    elif len(results) == 0:
      return None
    else: # TODO clean up - how are these collection connectors consistently dealing with the [ObjectId] type?
      result = results[0]
      result['_id'] = str(result['_id'])
      return result


  def get_documents(self, query: dict) -> dict:
      """
      Get a documents, given a query
      """
      assert isinstance(query, dict)
      result_list = list(self.collection.find(query))
      for result in result_list: # TODO clean up, as above
        result['_id'] = str(result['_id'])

      return list(result_list)


  def push_document(self, document) -> ObjectId:
    """
    Insert a [document] and get the _id it gets mapped to
    """
    assert isinstance(document, dict)

    result = self.collection.insert_one(document)
    return result.inserted_id


  def push_documents(self, documents: list) -> list:
    """
    Insert a list of [lexemes] and get the _ids that they map to
    """
    # TODO what if some fail?
    assert all(isinstance(document, dict) for document in documents)
    results = self.collection.insert_many(documents)
    return list(map(str, results.inserted_ids))
    

  def delete_document(self, query: dict) -> None:
    """
    Delete a single document, given a query
    """
    assert isinstance(query, dict)
    document = self.get_document(query)
    _id = document['_id']
    self.collection.delete_one({'_id': ObjectId(_id)})


  def delete_documents(self, query: dict) -> None:
    """
    Delete documents, given a [query]

    https://stackoverflow.com/a/18567093
    """
    assert isinstance(query, dict)
    self.collection.delete_many(query)

  
  def update_document(self, query, document) -> ObjectId:
    """
    Update a [document] and get the _id it gets mapped to
    """
    assert isinstance(document, dict)
    self.collection.update_one(query, {"$set": document})


# main
def main():
  ds_client = MongoClient("mongodb://localhost:27017/")
  db = CollectionConnector(ds_client, 'polish', 'lexicon')
  print(list(db.collection.find({'lemma': 'z'})))


if __name__ == "__main__":
  main()
