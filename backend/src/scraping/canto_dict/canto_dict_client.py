from fuzzywuzzy import fuzz
from scraping import get_soup_from_url
from scraping.canto_dict.query import query_jyutping, query_english, query_character
from scraping.canto_dict.search_results_scraping import get_search_results, get_results_redirect_link
from scraping.canto_dict.entry_scraping import get_dictionary_word_summary, get_dictionary_character_summary


def get_facts_from_jyutping(query: str, count: int=5):
    """
    TODO
    """
    query_results_soup = query_jyutping(query)
    results = sorted((get_search_results(query_results_soup)), key=(lambda x: fuzz.ratio(x['jyutping'], query)
), reverse=True)[:count]
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


def get_fact_from_jyutping(query: str):
    """
    TODO
    """
    return get_facts_from_jyutping(query, count=1)[0]


def get_fact_from_character(query: str):
    """
    TODO
    """
    assert len(query) == 1

    query_results_soup = query_character(query)
    
    with open('out.html', 'w') as file: # TODO remove
        file.write(str(query_results_soup))

    redirect_link = get_results_redirect_link(query_results_soup)

    if redirect_link: # I'm assuming the redirect will go to a single character page
        character_page = get_soup_from_url(redirect_link)
        return get_dictionary_character_summary(character_page)
    else:
        return None


def get_facts_from_english(query: str, count: int=5):
    """
    TODO
    """
    query_results_soup = query_english(query)
    results = get_search_results(query_results_soup)[:count]
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
    # print(get_fact_from_character('人'))
    print(get_fact_from_character('曇'))