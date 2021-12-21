#%% imports



#%% utils
def annotate_text(text, language_datastore, discovery_mode=False):
  """
  Take in a piece of text and annotate it using data from the given language_datastore

  If [discovery_mode]==[True], unknown terms will be added to the [language_datastore]
  """
  terms = list(map(lambda x: x.lower(), re.findall(r'\w+', text)))
  annotations = []

  for term in terms:
    language_datastore.get_lexeme