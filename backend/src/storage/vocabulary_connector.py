# imports
from copy import deepcopy

from bson.objectid import ObjectId
from storage.collection_connector import CollectionConnector
from storage.datastore_utils import generate_query
from training.sm2.stats import Stats, StatsDecoder

# constants
COLLECTION = "vocabulary"


class VocabularyConnector(CollectionConnector):
    """
    A [CollectionConnector] used specifically for recording terms known by a given user
    """

    def __init__(self, uri, language):
        """
        Constructor
        """
        language = language.lower()
        super(VocabularyConnector, self).__init__(uri, language, COLLECTION)
        self.language = language

    def get_deserialized_document(self, document: dict) -> dict:
        """
        Deserialize the datastore document into an in-memory python dictionary

        Args:
            document (dict): the document from the datastore

        Returns:
            dict: the in-memory python dictionary
        """
        dictionary = deepcopy(document)
        dictionary['stats'] = Stats(**dictionary['stats'])
        return dictionary

    def push_vocabulary_entry(self, lexeme_id: str, stats: Stats, user_id: str) -> str:
        """
        Add a new vocabulary entry to the datastore, represented by a [lexeme_id], [stats], and [user_id]
        """
        assert type(stats) == Stats

        entry = {'lexeme_id': ObjectId(
            lexeme_id), 'stats': stats.to_json(), 'user_id': ObjectId(user_id)}

        return super(VocabularyConnector, self).push_document(entry)

    def push_vocabulary_entries(self, entries: list) -> list:
        """
        Add list of vocabulary entries to the datastore, each represented by a dictionary

        dictionaries must contain 'lexeme_id', 'user_id', and 'stats'
        """
        assert isinstance(entries, list)

        for entry in entries:
            assert isinstance(entry, dict)
            assert all(key in entry for key in [
                       'lexeme_id', 'user_id', 'stats']), "Each vocabulary entry must contain a lexeme_id, user_id, and stats"
            assert isinstance(entry['stats'], Stats)
            entry['lexeme_id'] = ObjectId(entry['lexeme_id'])
            entry['user_id'] = ObjectId(entry['user_id'])
            entry['stats'] = entry['stats'].to_json()

        return super(VocabularyConnector, self).push_documents(entries)

    def get_vocabulary_entry(self, lexeme_id: str, user_id: str) -> dict:
        """
        Get a vocabulary entry and its _id, given the [lexeme_id] and [user_id] if it exists - otherwise, return an empty dictionary
        """
        assert lexeme_id and user_id

        if lexeme_id:
            lexeme_id = ObjectId(lexeme_id)
        user_id = ObjectId(user_id)
        query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
        document = super(VocabularyConnector, self).get_document(query)
        return self.get_deserialized_document(document) if document else {}

    def get_vocabulary_entries(self, lexeme_ids: list, user_ids: list) -> dict:
        """
        Get vocabulary entries and their _ids, given the [lexeme_ids] and [user_ids]
        """
        assert user_ids

        if isinstance(lexeme_ids, list):
            lexeme_ids = list(map(ObjectId, lexeme_ids))
        elif lexeme_ids:
            lexeme_ids = ObjectId(lexeme_ids)

        if isinstance(user_ids, list):
            user_ids = list(map(ObjectId, user_ids))
        elif user_ids:
            user_ids = ObjectId(user_ids)

        query = generate_query(lexeme_id=lexeme_ids, user_id=user_ids)
        results = super(VocabularyConnector, self).get_documents(query)
        return list(map(lambda x: self.get_deserialized_document(x), results))

    def delete_vocabulary_entry(self, lexeme_id: str, user_id: str) -> dict:
        """
        Delete vocabulary data entry and its _id, given the [lexeme_id], [form], and [pos]
        """
        if lexeme_id:
            lexeme_id = ObjectId(lexeme_id)
        query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
        return super(VocabularyConnector, self).delete_document(query)

    def delete_vocabulary_entries(self, lexeme_ids: list, user_ids: list) -> dict:
        """
        Delete vocabulary data entries and their _ids, given the [lexeme_ids] and [user_ids]
        """
        # TODO would it ever make sense to query for multiple user IDs?
        if isinstance(lexeme_ids, list):
            lexeme_ids = list(map(ObjectId, lexeme_ids))
        elif lexeme_ids:
            lexeme_ids = ObjectId(lexeme_ids)

        if isinstance(user_ids, list):
            ser_ids = list(map(ObjectId, user_ids))
        elif user_ids:
            ser_ids = ObjectId(user_ids)

        query = generate_query(lexeme_id=lexeme_ids, user_id=user_ids)
        return super(VocabularyConnector, self).delete_documents(query)

    def update_vocabulary_entry(self, lexeme_id: str, stats: Stats, user_id: str) -> str:
        """
        Udpate an existing vocabulary entry to the datastore, represented by a [lexeme_id], [stats], and [user_id]
        """
        assert user_id
        assert isinstance(stats, Stats)

        # ignore saving the recall from the training session to the datastore - it will be reinstantiated during the next session
        try:
            stats.__dict__.pop('recall')
        except:
            pass

        entry = {'lexeme_id': ObjectId(
            lexeme_id), 'stats': stats.to_json(), 'user_id': ObjectId(user_id)}
        query = generate_query(
            lexeme_id=entry['lexeme_id'], user_id=entry['user_id'])
        return super(VocabularyConnector, self).update_document(query, entry)

    def update_vocabulary_entries(self, entries: list) -> list:
        """
        Add list of vocabulary entries to the datastore, each represented by a dictionary

        dictionaries must contain 'lexeme_id', 'user_id', and 'stats'
        """
        assert isinstance(entries, list)

        for entry in entries:
            assert isinstance(entry, dict)
            assert all(key in entry for key in [
                       'lexeme_id', 'user_id', 'stats']), "Each vocabulary entry must contain a lexeme_id, user_id, and stats"
            assert isinstance(entry['stats'], Stats)

            entry['lexeme_id'] = ObjectId(entry['lexeme_id'])
            entry['user_id'] = ObjectId(entry['user_id'])
            query = generate_query(
                lexeme_id=entry['lexeme_id'], user_id=entry['user_id'])
            super(VocabularyConnector, self).update_document(query, entry)


# %% main
def main():
    pass


if __name__ == "__main__":
    main()
