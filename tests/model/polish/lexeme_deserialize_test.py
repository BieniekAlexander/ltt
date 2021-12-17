#%% imports
from json.decoder import JSONDecoder
import os, sys, json, pytest, requests
from bs4 import BeautifulSoup


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from scraping.wiktionary_extract_utils import extract_lexeme
from model.lexeme import LexemeDecoder, LexemeEncoder
from model.part_of_speech import PartOfSpeech
from model.polish.pos.particle import Particle

#%% pytest fixtures


#% tests
def test_deserialize_polish_lexeme_basic():
  json_str = open('tests/model/polish/data/particle_niemal.json').read()
  lexeme = json.loads(json_str, cls=LexemeDecoder)
  
  assert lexeme.lemma == "niemal"
  assert 'almost, nearly, practically' in lexeme.definitions[0]
  assert lexeme.pos == PartOfSpeech.PARTICLE


def test_deserialize_polish_lexeme_special_characters():
  json_str = open('tests/model/polish/data/conjunction_choc.json').read()
  lexeme = json.loads(json_str, cls=LexemeDecoder)
  
  assert lexeme.lemma == "choć"


def test_deserialize_polish_lexeme_encoded_characters():
  json_str = open('tests/model/polish/data/conjunction_chociaz.json').read()
  lexeme = json.loads(json_str, cls=LexemeDecoder)
  
  assert lexeme.lemma == "chociaż"


def test_deserialize_polish_adjective():
  json_str = open('tests/model/polish/data/adjective_czerwony.json').read()
  lexeme = json.loads(json_str, cls=LexemeDecoder)
  
  assert lexeme.lemma == "czerwony"
  assert 'red' in lexeme.definitions[0]
  assert lexeme.pos == PartOfSpeech.ADJECTIVE
  print(lexeme.inflections)
  assert lexeme.inflections['S']['F']['A'] == "czerwoną"


def test_deserialize_polish_noun():
  json_str = open('tests/model/polish/data/noun_pies.json').read()
  lexeme = json.loads(json_str, cls=LexemeDecoder)
  
  assert lexeme.lemma == "noun"
  assert 'dog' in lexeme.definitions[0]
  assert lexeme.pos == PartOfSpeech.NOUN
  assert lexeme.inflections['P']['I'] == "psami"


def test_deserialize_polish_noun():
  json_str = open('tests/model/polish/data/noun_pies.json').read()
  lexeme = json.loads(json_str, cls=LexemeDecoder)
  
  assert lexeme.lemma == "pies"
  assert 'dog' in lexeme.definitions[0]
  assert lexeme.pos == PartOfSpeech.NOUN
  assert lexeme.inflections['P']['I'] == "psami"


def test_encoding_invertible_polish_noun():
  lemma, pos, language = "kot", "Noun", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)

  json_str = json.dumps(lexeme, cls=LexemeEncoder)
  decoded_lexeme = json.loads(json_str, cls=LexemeDecoder)
  assert lexeme == decoded_lexeme


#%% main
def main():
  test_deserialize_polish_lexeme_special_characters()


if __name__ == "__main__":
  main()