# imports
import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from storage.datastore_utils import generate_query


# TODO I might remove this entirely, it might just make the most sense to use collections natively
class CollectionConnector:
    """
    An interface that lets us connect to a document store 
    """

    def __init__(self, datastore_client: MongoClient, database_name: str, collection_name: str, connector_schema: dict):
        """
        Establish an initial connection to the document store
        """
        self.collection = datastore_client[database_name][collection_name]
        self.connector_schema = connector_schema

    def get_document(self, query: dict) -> dict:
        """
        Wrapper for getting documents from datastore, given a [query]
        """
        results = self.get_documents(query)

        if len(results) > 1:
           # TODO make specific error type
            raise Exception(
                f"Found more than one result when trying to get a document, given a query - '{query}'")
        elif len(results) == 0:
            return None
        # TODO clean up - how are these collection connectors consistently dealing with the [ObjectId] type?
        else:
            result = results[0]
            return result

    def get_documents(self, query: dict) -> dict:
        """
        Get a documents, given a query
        """
        return list(self.collection.find(query))
        
    def push_document(self, document) -> ObjectId:
        """
        Insert a [document] and get the _id it gets mapped to
        """
        assert isinstance(document, dict)

        result = self.collection.insert_one(document)
        return ObjectId(result.inserted_id)

    def push_documents(self, documents: list) -> list[ObjectId]:
        """
        Insert a list of [lexemes] and get the _ids that they map to
        """
        # TODO what if some fail?
        assert all(isinstance(document, dict) for document in documents)
        results = self.collection.insert_many(documents)
        return results.inserted_ids

    def delete_document(self, query: dict) -> None:
        """
        Delete a single document, given a query
        """
        document = self.get_document(query)
        _id = document['_id']
        self.collection.delete_one({'_id': ObjectId(_id)})

    def delete_documents(self, query: dict) -> None:
        """
        Delete documents, given a [query]

        https://stackoverflow.com/a/18567093
        """
        self.collection.delete_many(query)

    def update_document(self, query: dict, document: dict) -> None:
        """
        Update a [document] and get the _id it gets mapped to
        """
        if list(self.collection.find(query)) == []:
            raise Exception("No documents to update found")

        self.collection.update_one(query, {"$set": document})


# main
def main():
    from storage.datastore_schemata.chinese_schemata import character_schema as zh_character_schema
    import os

    ds_client = MongoClient(os.getenv('MONGODB_URI'))
    chinese_character_connector = CollectionConnector(ds_client, 'chinese', 'lexicon', zh_character_schema['$jsonSchema'])
    # chinese_character_connector.push_document({'lemma': 'wow'})

if __name__ == "__main__":
    main()
