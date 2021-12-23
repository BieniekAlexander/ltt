# imports
import pymongo, logging
from bson.objectid import ObjectId

# constants


class CollectionConnector(object):
  """
  An interface that lets us connect to a document store 
  """
  def __init__(self, uri: str, database_name: str, collection_name: str):
    """
    Establish an initial connection to the document store
    """
    self.client = pymongo.MongoClient(uri)
    self.db = self.client.admin

    if self.db.command("serverStatus"):
      logging.info("Connected to mongodb and got server status")

    self.db = self.client[database_name]
    self.collection = self.db[collection_name]


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
    else:
      return results[0]


  def get_documents(self, query: dict) -> dict:
      """
      Get a documents, given a query
      """
      assert isinstance(query, dict)
      result_set = self.collection.find(query)
      return list(result_set)


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


# main
def main():
  db = CollectionConnector("mongodb://localhost:27017/", 'lexicon', 'polish')
  print(list(db.collection.find({'lemma': 'z'})))


if __name__ == "__main__":
  main()

  