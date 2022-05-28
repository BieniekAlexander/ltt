# tests for utilities for scraping tables from html
#% imports
# pytest testing that exceptions are raised - https://stackoverflow.com/a/29855337
import os, sys, json, pytest, requests, time
from bs4 import BeautifulSoup


from scraping.wiktionary_spider import WiktionarySpider


#% tests
def test_query_czerwony_polish():
  form, language = "czerwony", "Polish"
  spider = WiktionarySpider()
  results = spider.query_lexemes(form, language)
  
  assert 'https://en.wiktionary.org/wiki/czerwony' in spider.steps
  assert len(results) == 2
  
  for lexeme in results:
    assert lexeme.lemma == "czerwony"


def test_query_czerwony_polish_adjective():
  form, pos, language = "czerwony", 'adjective', "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
   
  assert 'https://en.wiktionary.org/wiki/czerwony' in spider.steps
  assert lexeme.lemma == "czerwony"
  assert lexeme.pos.value == "ADJECTIVE"


def test_query_zimna_polish():
  # note: the scraper also finds zimno (adverb) when it jumps to that page, though "zimna" is not a form of it
  form, language = "zimna", "Polish"
  spider = WiktionarySpider()
  results = spider.query_lexemes(form, language)
  
  assert 'https://en.wiktionary.org/wiki/zimna' in spider.steps
  assert len(results) >= 2
  
  parts_of_speech = list(map(lambda x: x.pos.value, results))
  assert all(pos in parts_of_speech for pos in ['NOUN', 'ADJECTIVE'])


def test_query_zimna_polish_adjective():
  form, pos, language = "zimna", 'adjective', "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
  
  assert 'https://en.wiktionary.org/wiki/zimna' in spider.steps
  assert 'https://en.wiktionary.org/wiki/zimny' in spider.steps
  assert lexeme.lemma == "zimny"
  assert lexeme.pos.value == "ADJECTIVE"


def test_query_zimna_polish_noun():
  form, pos, language = "zimna", 'noun', "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
  
  assert 'https://en.wiktionary.org/wiki/zimna' in spider.steps
  assert 'https://en.wiktionary.org/wiki/zimno' in spider.steps
  assert lexeme.lemma == "zimno"
  assert lexeme.pos.value == "NOUN"


def test_get_lexeme_special_characters():
  form, pos, language = "miłość", "noun", "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
  
  assert lexeme.lemma == "miłość"
  

def test_get_lexeme_special_characters_alternate_form():
  # TODO - address failing case - miłości's first few search results are wrong, maybe I should collect the lexeme result and verify that the initial form I queried with is in the inflection table
  # https://en.wiktionary.org/w/index.php?search=mi%C5%82o%C5%9B%C4%87i&title=Special:Search&profile=advanced&fulltext=1&searchengineselect=mediawiki&ns0=1
  form, pos, language = "miłośći", "Noun", "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
  
  assert lexeme.lemma == "miłość"
  

def test_get_lexeme_special_characters_uses_search():
  form, pos, language = "niemożliwe", "Adjective", "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
  print(spider.steps)
  
  assert lexeme.lemma == "niemożliwy"


def test_get_lexeme_no_pos():
  form, language = "piekło", "Polish"
  spider = WiktionarySpider()
  results = spider.query_lexemes(form, language)
  lexeme = results[0]
  
  assert lexeme.lemma == "piekło"
  assert lexeme.pos.value == "NOUN"
  

def test_get_lexeme_no_pos_alternate_form():
  # this can potentially find piec - VERB, piec - NOUN, and piekło - NOUN
  form, language = "piekła", "Polish"
  spider = WiktionarySpider()
  results = spider.query_lexemes(form, language)

  parts_of_speech = list(map(lambda x: x.pos.value, results))
  lemmas = list(map(lambda x: x.lemma, results))
  
  assert all(pos in parts_of_speech for pos in ['VERB', 'NOUN'])
  assert all(lemma in lemmas for lemma in ['piekło', 'piec'])


def test_get_lexeme_form_is_lemma_of_other_pos_in_page():
  form, pos, language = "piekło", "Verb", "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
  
  assert lexeme.lemma == "piec"
  assert lexeme.pos.value == "VERB"


def test_get_lexeme_multiple_non_lemma_forms_in_page():
  form, pos, language = "piekła", "Verb", "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
  
  assert lexeme.lemma == "piec"
  assert lexeme.pos.value == "VERB"


def test_get_lexeme_none():
  form, pos, language = "zničit", "Verb", "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
  
  assert lexeme == None


def test_get_lexeme_search_results_none():
  form, pos, language = "zničeno", "Verb", "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)
  
  assert lexeme == None


def test_get_lexeme_multiple_steps():
  form, pos, language = "swe", "Pronoun", "Polish"
  spider = WiktionarySpider()
  lexeme = spider.query_lexeme(form, pos, language)

  assert lexeme.lemma == "swój"
  assert lexeme.pos.value == "PRONOUN"
  
  

#% main
def main():
  pass
  

if __name__ == "__main__":
  main()