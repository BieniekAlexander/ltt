# imports

from bson.objectid import ObjectId
from language.lexeme import Lexeme
from language.part_of_speech import PartOfSpeech
from language.polish.pos.preposition import Preposition
from pymongo import MongoClient
from storage.collection_connector import CollectionConnector
from storage.datastore_utils import cast_enum_to_str, generate_query

# constants
COLLECTION = "lexicon"


class LexiconConnector(CollectionConnector):
    """
    A [DocumentStoreConnector] used specifically for interacting with a language's lexicon
    """

    def __init__(self, datastore_client: MongoClient, language: str):
        language = language.lower()
        super(LexiconConnector, self).__init__(
            datastore_client, language, COLLECTION)
        self.language = language

    def get_lexeme_entry(self, lemma=None, pos=None, _id=None) -> dict:
        """
        Get the lexeme entry, given either an [_id] or a [lemma] and/or [pos]
        """
        # preprocess args
        assert bool(_id) ^ bool(
            lemma or pos), "supply either _ids, or lemmas and/or poses"

        if _id:
            _id = ObjectId(_id)
        else:
            if pos:
                pos = cast_enum_to_str(pos)

        query = generate_query(lemma=lemma, _id=_id, pos=pos)
        return super(LexiconConnector, self).get_document(query)

    def get_lexeme_entries(self, lemmas=None, poses=None, _ids=None) -> dict:
        """
        Get (id, [Lexeme] [dict]) mappings, given either [_ids], or [lemmas] and/or [poses]
        """
        # preprocess args
        assert bool(_ids) ^ bool(
            lemmas or poses), "supply either _ids, or lemmas and/or poses"

        if _ids:
            assert isinstance(_ids, list)
            _ids = list(map(ObjectId, _ids))
        else:
            if lemmas:
                assert isinstance(lemmas, list)
            if poses:
                assert isinstance(poses, list)
                poses = list(map(cast_enum_to_str, poses))

        query = generate_query(lemma=lemmas, _id=_ids, pos=poses)
        return super(LexiconConnector, self).get_documents(query)

    def cast_lexeme_dictionary(self, lexeme) -> dict:
        """
        Cast a [lexeme] to a dictionary type if it's not already a dictionary

        TODO this might be a silly utility to provide, maybe just have the user provide a dictionary from their end
        """
        assert isinstance(lexeme, dict) or isinstance(lexeme, Lexeme)

        if isinstance(lexeme, Lexeme):
            return lexeme.to_json()
        else:
            return lexeme

    def push_lexeme_entry(self, lexeme) -> ObjectId:
        """
        Insert a [Lexeme] and get its [ObjectId]
        """
        lexeme_dict = self.cast_lexeme_dictionary(lexeme)
        return super(LexiconConnector, self).push_document(lexeme_dict)

    def push_lexeme_entries(self, lexemes) -> list:
        """
        Insert a list of [lexemes] and get a list of their [ObjectId]s
        """
        # TODO what if some fail?
        assert lexemes \
            and isinstance(lexemes, list) \
            and all(isinstance(lexeme, Lexeme) or isinstance(lexeme, dict) for lexeme in lexemes)

        lexeme_dicts = list(
            map(lambda x: self.cast_lexeme_dictionary(x), lexemes))
        return super(LexiconConnector, self).push_documents(lexeme_dicts)

    def delete_lexeme_entry(self, lemma=None, pos=None, _id=None) -> None:
        """
        Delete a [Lexeme] dictionary, given either an [_id] or a [lemma] and/or [pos]
        """
        # preprocess args
        assert bool(_id) ^ bool(
            lemma or pos), "supply either _ids, or lemmas and/or poses"

        if _id:
            _id = ObjectId(_id)
        else:
            if pos:
                pos = cast_enum_to_str(pos)

        query = generate_query(lemma=lemma, _id=_id, pos=pos)
        return super(LexiconConnector, self).delete_document(query)

    def delete_lexeme_entries(self, lemmas=None, poses=None, _ids=None):
        """
        Delete [Lexeme] dictionaries, given either [_ids], or [lemmas] and/or [poses]

        https://stackoverflow.com/a/18567093
        """
        # preprocess args
        assert bool(_ids) ^ bool(
            lemmas or poses), "supply either _ids, or lemmas and/or poses"

        if _ids:
            assert isinstance(_ids, list)
            _ids = list(map(ObjectId, _ids))
        else:
            if lemmas:
                assert isinstance(lemmas, list)
            if poses:
                assert isinstance(poses, list)
                poses = list(map(cast_enum_to_str, poses))

        mappings = self.get_lexeme_entries(
            lemmas=lemmas, poses=poses, _ids=_ids)
        query = generate_query(lemma=lemmas, _id=_ids)
        return super(LexiconConnector, self).delete_documents(query)


# main
def main():
    ds_client = MongoClient("mongodb://localhost:27017/")
    polish_lexicon = LexiconConnector(ds_client, 'polish')
    lemmas = ['aaa', 'bbb', 'ccc']
    lexemes = [Preposition(l, PartOfSpeech.PREPOSITION, [], [])
               for l in lemmas]
    polish_lexicon.push_lexeme_entries(lexemes)

    polish_lexicon.delete_lexeme_mappings(lemmas=lemmas)


if __name__ == "__main__":
    main()
