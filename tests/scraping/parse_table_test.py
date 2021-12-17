# tests for utilities for scraping tables from html
#% imports
import os, sys, json
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from scraping.html_parse_utils import parse_inflection_table


#% tests
def test_parse_pl_noun_ptak():
  truth = json.loads(open('tests/scraping/data/ptak_inflections.json', 'r').read())
  html = open('tests/scraping/data/ptak_inflections.html').read()
  soup = BeautifulSoup(html, "html.parser")
  table = soup.table
  parsed = parse_inflection_table(table)
  assert parsed == truth


def test_parse_pl_adjective_czerwony():
  truth = json.loads(open('tests/scraping/data/czerwony_inflections.json', 'r').read())
  html = open('tests/scraping/data/czerwony_inflections.html').read()
  soup = BeautifulSoup(html, "html.parser")
  table = soup.table
  parsed = parse_inflection_table(table)
  print(parsed)
  assert parsed == truth


def test_parse_pl_adjective_biec():
  truth = json.loads(open('tests/scraping/data/biec_inflections.json', 'r').read())
  html = open('tests/scraping/data/biec_inflections.html').read()
  soup = BeautifulSoup(html, "html.parser")
  table = soup.table
  parsed = parse_inflection_table(table)
  print(parsed)
  assert parsed == truth


#% main
def main():
  test_parse_pl_adjective_czerwony()


if __name__ == "__main__":
  main()