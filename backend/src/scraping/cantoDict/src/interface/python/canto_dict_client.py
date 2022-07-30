# imports
from fuzzywuzzy import fuzz

from scraping.wiktionary_crawl_utils import get_soup
from src.crawling.query import query_jyutping, query_english
from src.scraping.search_results_scraping import get_search_results
from src.scraping.entry_scraping import get_dictionary_word_summary, get_dictionary_character_summary


def get_facts_from_jyutping(query: str, count: int = 5):
    """
    TODO
    """
    # sort results by similarity to query - in my experience, the list results aren't ordered as such already, see "m4"
    query_results_soup = query_jyutping(query) # TODO think aobut how we're handling web requests
    results = sorted(get_search_results(query_results_soup), key=lambda x: fuzz.ratio(x['jyutping'], query), reverse=True)[:count]

    # TODO apply some filtering, ex: what if I know that I want the jau5 character that is about having something, can I add that as a constraint

    facts = []
    for result in results:
        url = result['url']
        soup = get_soup(url)

        if 'words' in url: scraper = get_dictionary_word_summary
        elif 'characters' in url: scraper = get_dictionary_character_summary

        facts.append(scraper(soup))

    return facts

def get_fact_from_jyutping(query: str):
    """
    TODO
    """
    return get_facts_from_jyutping(query, count=1)[0]

def get_facts_from_english(query: str, count: int = 5):
    """
    TODO
    """
    query_results_soup = query_english(query) # TODO think aobut how we're handling web requests
    results = get_search_results(query_results_soup)[:count]
    # TODO I think I need to do some sorting here to rank the quality of the results

    facts = []
    for result in results:
        url = result['url']
        soup = get_soup(url)

        if 'words' in url: scraper = get_dictionary_word_summary
        elif 'characters' in url: scraper = get_dictionary_character_summary

        facts.append(scraper(soup))

    return facts

def get_fact_from_english(query: str):
    """
    TODO
    """
    return get_facts_from_english(query, count=1)[0]

def get_facts_from_character(query: str, count: int = 5):
    """
    TODO if I search for 茶, it reroutes me to the page for it, how do I handle this?
    there are also different searches for (a single) character, and then I'm assuming "Chinese words" comprised of multiple characters

    # http://www.cantonese.sheik.co.uk/dictionary/characters/292/
    """
    pass

def get_fact_from_character(query: str):
    """
    TODO
    """
    return get_facts_from_character(query, count=1)[0]