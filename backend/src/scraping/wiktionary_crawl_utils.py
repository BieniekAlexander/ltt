# %% imports
import requests
from bs4 import BeautifulSoup
from scraping import get_soup_from_url, get_wiktionary_term_url


# %% utils
def is_no_entries_page(soup):
    """
    Returns true if this page indicates that no entries were found

    ex: https://en.wiktionary.org/wiki/awdoiawjido
    """
    return bool(soup.find('div', {'class': 'noarticletext'}))


def is_entries_page(soup):
    """
    Returns true if the page has lexeme entries

    ex: https://en.wiktionary.org/wiki/czerwony  
    """
    return bool(soup.find('div', {'class': 'mw-parser-output'}))


def is_search_results_page(soup):
    """
    Returns true if this wiktionary webpage is a search results webpage

    ex: https://en.wiktionary.org/w/index.php?search=wygodnym&title=Special%3ASearch&go=Go&ns0=1
    """
    return bool(soup.find('ul', {'class': 'mw-search-results'})) \
        or bool(soup.find('p', {'class': 'mw-search-nonefound'}))


def get_search_result_links(soup, domain_name="https://en.wiktionary.org"):
    """
    Returns the linked articles in a [soup] wiktionary search results page

    Asserts that the page is a wiktionary search results page
    """
    assert is_search_results_page(soup)

    search_results_ul = soup.find('ul', {'class': 'mw-search-results'})

    if search_results_ul:  # this is a searh results page with no entries
        search_results_lis = list(
            search_results_ul.find_all('li', recursive=False))
        return [domain_name+li.find('a')['href'] for li in search_results_lis]
    else:  # this is a searh results page with no entries
        return []


# %% main
def main():
    soup = get_soup_from_url(get_wiktionary_term_url('czerwony'))
    print(type(soup))


if __name__ == "__main__":
    main()
