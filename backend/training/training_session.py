from storage.datastore_client import DatastoreClient
from storage.language_datastore import LanguageDatastore
from storage.lexicon_connector import LexiconConnector
from training.recall import Recall
from training.stats import Stats, StatsComparison


# constants
MONGODB_URL = "mongodb://localhost:27017/"


class TrainingSession(object):
  def __init__(self, user_id: str, language: str, datastore_client: DatastoreClient):
    """
    An object that represents a user's session for studying terms
    
    TODO What will this class do? Will it have subclasses? how will this generalize? for now, I just want to get, guess, and score terms

    Args:
        user_id (str): The ID of the user who is testing their vocabulary
        language (str): The language that the user is training
    """
    self.user_id = user_id
    self.language = language
    self.language_datastore = LanguageDatastore(datastore_client, language)
    self.lexicon_connector = LexiconConnector(datastore_client, language)
    self.study_terms = None
    self.in_sync = False # flag to indicate whether the state of the vocabulary in memory reflects the vocabulary in the datastore
    self.stats_comparison = StatsComparison()


  def __del__(self):
    """
    When the object is destroyed, overwrite the study terms in the datastore
    """
    self.save_study_terms()
    

  def load_study_terms(self):
    """
    Collects the vocabulary being used by the user in the training session
    """
    # get the terms and the user's vocab entries
    vocabulary = sorted(self.language_datastore.get_vocabulary_entries(lexeme_ids = [], user_id = self.user_id), key=lambda x: x['lexeme_id'])
    lexeme_ids = list(map(lambda x: x['lexeme_id'], vocabulary))
    lexemes = sorted(self.lexicon_connector.get_lexeme_entries(_ids = lexeme_ids), key=lambda x: x['_id'])
    study_terms = []

    # join the terms and vocab entries on the id
    for v, l in zip(vocabulary, lexemes):
      assert str(v['lexeme_id']) == str(l['_id']), f"'{v['lexeme_id']}' != '{l['_id']}'"
      study_terms.append({'term': l, **v})
    
    self.study_terms = sorted(study_terms, key=lambda x: x['stats'].rating)
    self.in_sync = True

  
  def save_study_terms(self):
    """
    Writes the updated study terms to the datastore
    """
    assert self.study_terms != None, "Study terms not loaded"
    
    if not self.in_sync:
      for term in self.study_terms:
        if term['stats'].rating > 1.0: print(term['stats'])
        self.language_datastore.update_vocabulary_entry(lexeme_id=term['lexeme_id'], stats=term['stats'], user_id=self.user_id)

    self.in_sync = True


  def get_study_term(self):
    """
    Gets the next term to be studied
    """
    assert self.study_terms != None, "Study terms not loaded"
    return self.study_terms[0]

  
  def update_study_term_stats(self, study_term: str, recall: Recall):
    """
    Update the stats of a study term and indicate that the set of study terms is out of sync with the datastore

    Args:
        lexeme_id (str): the [_id] of the term to update
        stats (dict): the new [stats] of the study term
    """
    # update stats
    multipliers = {
      Recall.UNKNOWN: .5,
      Recall.BAD: .9,
      Recall.OKAY: 1.0,
      Recall.GOOD: 1.1,
      Recall.KNOWN: 2
    }
    study_term['stats'].rating = study_term['stats'].rating * multipliers[recall]
    
    self.study_terms = sorted(self.study_terms, key=lambda x: x['stats'].rating)
    self.in_sync = False


def main():
  datastore_client = DatastoreClient(MONGODB_URL)
  training_session = TrainingSession('a'*24, 'polish', datastore_client)
  training_session.load_study_terms()

  term = training_session.get_study_term()
  training_session.update_study_term_stats(term, stats=Stats(rating=term['stats'].rating*1.05))
  training_session.save_study_terms()


if __name__ == "__main__":
  main()