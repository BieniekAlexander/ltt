from fuzzywuzzy import fuzz
from enforce_typing import enforce_types
from scraping import get_soup_from_url
from scraping.canto_dict.query import query_jyutping, query_english, query_character, query_word
from scraping.canto_dict.search_results_scraping import get_results_redirect_link, get_search_results_map, get_all_search_results
from scraping.canto_dict.entry_scraping import get_dictionary_word_summary, get_dictionary_character_summary


def get_facts_from_jyutping(query: str, count: int=5):
    """
    TODO
    """
    query_results_soup = query_jyutping(query)
    alL_results = get_all_search_results(query_results_soup)
    results = sorted(alL_results, key=(lambda x: fuzz.ratio(x['jyutping'], query)), reverse=True)[:count]
    facts = []

    for result in results:
        url = result['url']
        soup = get_soup_from_url(url)
        if 'words' in url:
            scraper = get_dictionary_word_summary
        else:
            if 'characters' in url:
                scraper = get_dictionary_character_summary
        facts.append(scraper(soup))

    return facts

@enforce_types
def get_fact_from_jyutping(query: str):
    """
    TODO
    """
    return get_facts_from_jyutping(query, count=1)[0]

@enforce_types
def get_fact_from_characters(query: str) -> dict:
    """
    TODO
    """
    assert len(query) > 0

    if len(query) == 1:
        return get_fact_from_character(query)
    else: 
        return get_fact_from_word(query)

@enforce_types
def get_fact_from_word(query: str, max_result_scan: int = 5) -> dict:
    """
    TODO
    """
    assert len(query) > 1

    query_results_soup = query_word(query)
    search_results_map = get_search_results_map(query_results_soup)
    word_search_results = search_results_map['words']
    
    if word_search_results == None:
        return None

    for row in word_search_results[:max_result_scan]:
        # NOTE - every result in the results page lists traditional characters,
        # so if I search with simplified characters, the correct word might not have the same representation
        if len(row['entry']) == len(query):
            word_soup = get_soup_from_url(row['url'])
            fact = get_dictionary_word_summary(word_soup)

            if fact['word'] == row['entry']:
                return fact

    return None

@enforce_types
def get_fact_from_character(query: str, max_result_scan: int = 5) -> dict:
    """
    TODO

    NOTE: A single simplified character can return multiple traditional characters - if this function returns nothing, that 
    """
    assert len(query) == 1

    query_results_soup = query_character(query)    
    redirect_link = get_results_redirect_link(query_results_soup)

    if redirect_link: # I'm assuming the redirect will go to a single character page
        character_page = get_soup_from_url(redirect_link)
        return get_dictionary_character_summary(character_page)
    else: # if we weren't redirected, then we'll have to scan a bit to find the character
        query_results_character_entries = get_search_results_map(query_results_soup)['characters']
        if query_results_character_entries == None: return None

        for entry in query_results_character_entries:
            character_url = entry['url']
            character_soup = get_soup_from_url(character_url)
            fact = get_dictionary_character_summary(character_soup)

            if fact['word'] == query:
                return fact
        
        return None

@enforce_types
def get_facts_from_english(query: str, count: int=5):
    """
    TODO
    """
    query_results_soup = query_english(query)
    results = get_all_search_results[:count]

    facts = []
    for result in results:
        url = result['url']
        soup = get_soup_from_url(url)
        if 'words' in url:
            scraper = get_dictionary_word_summary
        else:
            if 'characters' in url:
                scraper = get_dictionary_character_summary
        facts.append(scraper(soup))

    return facts


def get_fact_from_english(query: str):
    """
    TODO
    """
    pass


def get_character_from_jyutping(query: str):
    """
    TODO
    """
    pass


if __name__ == "__main__":
    print(get_fact_from_characters('女'))
    # print(get_fact_from_characters('爱'))