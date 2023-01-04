# %% imports
import logging
import re

from bson.objectid import ObjectId
from scraping.wiktionary_spider import WiktionarySpider
from storage.language_datastores.polish_datastore import PolishDatastore


# TODO this might be better off accessing mongodb directly
def annotate_text(text: str, language_datastore: PolishDatastore, language: str, user_id: ObjectId = None, discovery_mode: bool = False):
    """
    Take in a piece of text and annotate it using data from the given language_datastore

    If [discovery_mode]==[True], unknown terms will be added to the [language_datastore]
    """
    assert isinstance(text, str)

    terms = list(re.findall(r'\w+', text))
    annotations = []

    for i, term in enumerate(terms):
        # how are we identifying the most probable lexeme - especially if we don't know the POS?
        annotation = {'term': term}
        annotations.append(annotation)

        try:
            term = term.lower()  # lowercase the term for reading from database and scraping from wiktionary - TODO what to do about proper nouns?
            potential_lexeme_dictionary_mappings = language_datastore.get_lexemes_from_form(
                form=term.lower())

            # get lexeme from lexicon
            if potential_lexeme_dictionary_mappings:
                entry = potential_lexeme_dictionary_mappings[0]
                annotation['lexeme_id'] = str(entry.pop('_id'))
                annotation['lexeme'] = entry
            else:
                if discovery_mode:
                    spider = WiktionarySpider()
                    lexeme = spider.query_lexemes(term, language)[0]
                    annotation['lexeme'] = lexeme.to_json()
                    annotation['lexeme_id'] = str(language_datastore.add_lexeme(
                        lexeme))  # TOOD this requires a lexeme, fails on JSON?
                else:
                    logging.warning(
                        f"Failed to annotate the {i}th term - {term} (discovery disabled)")

            if 'lexeme' in annotation:
                # try to get lexeme from a user's vocabulary
                if user_id is not None:
                    entries = language_datastore.get_vocabulary_entries(
                        lexeme_id=[ObjectId(annotation['lexeme_id'])], user_id=user_id)

                    if len(entries) > 0:
                        entry = entries[0]
                        annotation['vocabulary_id'] = entry['vocabulary_id']
                        annotation['stats'] = entry['stats']
                    else:  # set to null to indicate that we tried to tie to vocabulary and found nothing
                        annotation['vocabulary_id'] = None
                        annotation['stats'] = None
        except Exception as e:
            logging.error(
                f"Tried & failed to scrape the {i}th term {term} - {e}")

    return annotations


def discover_lexeme(term, pos, language):
    """
    Search the internet for the given [term] in a given [pos] (if provided), in the given [language], and add it to the lexicon
    """
    return
