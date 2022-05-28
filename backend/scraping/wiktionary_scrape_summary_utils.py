#%% imports
from bs4.element import NavigableString, Tag
import requests
import sys, os
from bs4 import BeautifulSoup




#%% utils
def wiktionary_get_all_lang_pos_lemmas(soup):
  """
  From a page that lists the terms of a part of speech in a given language, get all lemmas

  example page: https://en.wiktionary.org/wiki/Category:Polish_prepositions
  """
  letter_divs = soup.find_all('div', {'class': 'mw-category-group'})
  lemmas = []

  for div in letter_divs:
    lemma_lis = div.find_all('li')
    
    for lemma_li in lemma_lis:
      lemmas.append(lemma_li.get_text())
    
  return lemmas


#%% main
def main():
    summary_page = f"https://en.wiktionary.org/wiki/Category:Polish_prepositions"
    page = requests.get(summary_page)
    soup = BeautifulSoup(page.content, "html.parser")
    lemmas = wiktionary_get_all_lang_pos_lemmas(soup)
    print(lemmas)


if __name__ == "__main__":
    main()