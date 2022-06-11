from pymongo import MongoClient


from storage.language_datastore import LanguageDatastore
from storage.lexicon_connector import LexiconConnector
from training.sm2.recall import Recall
from training.sm2.study_set import StudySet
from training.vocab import Vocab
from training.sm2.utils import get_repetition_interval


# TODO things to clean up:
# - training session vocab list vs study set


# constants
MONGODB_URL = "mongodb://localhost:27017/"


class TrainingSession(object):
  def __init__(self, user_id: str, language: str, datastore_client: MongoClient, interval: int = 1, count: int = 50):
    """
    An object that represents a user's session for studying terms
    
    Based on the Supermemory 2 Algorithm

    Args:
        user_id (str): The ID of the user who is testing their vocabulary
        language (str): The language that the user is training
    """
    self.user_id = user_id
    self.language = language
    self.language_datastore = LanguageDatastore(datastore_client, language)
    self.lexicon_connector = LexiconConnector(datastore_client, language)
    self.interval = interval
    self.count = count
    self.study_terms = None
    self.in_sync = False # flag to indicate whether the state of the vocabulary in memory reflects the vocabulary in the datastore


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
    self.study_terms = []

    # join the terms and vocab entries on the id
    for v, l in zip(vocabulary, lexemes):
      assert str(v['lexeme_id']) == str(l['_id']), f"'{v['lexeme_id']}' != '{l['_id']}'"
      vocab = Vocab(lexeme_id = (v['lexeme_id']), vocab_id=str(l['_id']), lexeme=l, stats=v['stats'])
      self.study_terms.append(vocab)
    
    self.study_set = StudySet(vocabulary=self.study_terms, count=self.count)
    self.in_sync = True

  
  def save_study_terms(self):
    """
    Writes the updated study terms to the datastore
    """
    assert self.study_terms != None, "Study terms not loaded"
    
    if not self.in_sync:
      for term in self.study_terms:
        if term.stats.recall:
          term.stats.repetition += 1
          term.stats.interval = get_repetition_interval(term.stats.repetition, term.stats.ef)
        self.language_datastore.update_vocabulary_entry(lexeme_id=term.lexeme_id, stats=term.stats, user_id=self.user_id)

    self.in_sync = True


  def get_study_entry(self):
    """
    Gets the next term to be studied
    """
    assert self.study_terms != None, "Study terms not loaded"
    return self.study_set.get_study_term()

  
  def update_study_entry_stats(self, term: dict, recall: Recall):
    """
    Update the stats of a study term and indicate that the set of study terms is out of sync with the datastore

    Args:
        term (dict): the term to update
        stats (Recall): the recall from the last repetition
    """
    term.stats.update(recall)
    self.in_sync = False


def main():
  datastore_client = MongoClient(MONGODB_URL)
  training_session = TrainingSession('a'*24, 'polish', datastore_client)
  training_session.load_study_terms()

  term = training_session.get_study_entry()
  training_session.update_study_entry_stats(term, Recall.GREAT)
  training_session.save_study_terms()


if __name__ == "__main__":
  main()