import logging
import re
from enforce_typing import enforce_types
from bs4 import BeautifulSoup

RESULT_TABLE_REGEX_PATTERN_DICT = {
    'characters': r'Found \d+ character entr(y|ies) for .*',
    'words': r'Found \d+ word entr(y|ies) for .*',
    'examples': r'Found \d+ Chinese Examples? for .*',
}

def get_results_redirect_link(soup: BeautifulSoup) -> str:
    """
    Return a redirect link from a cantodict search results page, if there exists one, otherwise return [None]
    """
    if "One character found, if your page does not redirect please" not in str(soup):
        return None

    return soup.find_all('a')[-1]['href']

def get_char_word_table_entries(results_table: BeautifulSoup) -> list[dict]:
    """
    Return a list parsed of entries from the BeautifulSoup table, specifically for the character and word tables
    """
    assert issubclass(BeautifulSoup, type(results_table))

    results_table_rows = results_table.find_all('tr')
    header_row_index = 0
    while not results_table_rows[header_row_index].td.has_attr('width'):
        header_row_index += 1

    results = []
    for i in range(header_row_index + 1, len(results_table_rows)):
        data_row = results_table_rows[i]
        tds = data_row.find_all('td')
        url = tds[0].a['href']
        entry = tds[1].span.text.strip()
        jyutping = tds[2].text.strip()
        pinyin = tds[3].text.strip()
        definition = tds[4].text.strip()
        results.append({'url':url, 
         'entry':entry, 
         'jyutping':jyutping,
         'pinyin': pinyin,
         'definitions':definition
          })

    return results

def get_example_table_entries(results_table: BeautifulSoup) -> list[dict]:
    """
    Return a list parsed of entries from the BeautifulSoup table, specifically for the example table

    TODO it looks like this parser is missing the very first example entry
    ex: search for word 可愛
    """
    results_table_rows = results_table.find_all('tr')
    header_row_index = 0
    while not results_table_rows[header_row_index].td.has_attr('width'):
        header_row_index += 1

    results = []
    for i in range(header_row_index + 1, len(results_table_rows)):
        data_row = results_table_rows[i]
        tds = data_row.find_all('td')
        url = tds[0].a['href']
        entry = tds[1].span.text.strip()
        definition = tds[2].text.strip()
        results.append({'url':url, 
         'entry':entry, 
         'definitions':definition
         })

    return results

def get_search_results_table_map(soup: BeautifulSoup) -> dict[str, BeautifulSoup]:
    """
    Get each BeautifulSoup table containing vocabulary entries
    """
    results_table_map = {table_type_key: None for table_type_key in RESULT_TABLE_REGEX_PATTERN_DICT}
    results_table = soup.find('table')
    
    while results_table:
        for table_type_key in RESULT_TABLE_REGEX_PATTERN_DICT:
            regex = re.compile(RESULT_TABLE_REGEX_PATTERN_DICT[table_type_key])
            
            try:
                result_table_header = results_table.tr.td.b.text
                
                if regex.search(result_table_header):
                    results_table_map[table_type_key] = results_table
                else:
                    logging.debug(f"header not matched - {result_table_header}")
                
            except Exception as e:
                logging.debug(f'table is not a results table, skipping')

        results_table = results_table.find_next('table')

    return results_table_map

def get_search_results_map(soup: BeautifulSoup) -> dict[str, list[dict]]:
    """
    Get a mapping of entry types to search result lists
    """
    results_table_map: dict = get_search_results_table_map(soup)
    results_map: dict = {table_type_key: None for table_type_key in RESULT_TABLE_REGEX_PATTERN_DICT}

    for key in results_table_map:
        if results_table_map[key] == None:
            continue
        elif key in ['characters', 'words']:
            results_map[key] = get_char_word_table_entries(results_table_map[key])
        elif key == 'examples':
            results_map[key] = get_example_table_entries(results_table_map[key])

    return results_map

def get_all_search_results(soup: BeautifulSoup) -> list[dict]:
    """
    Get all entries listed in the search results tables
    """
    search_results_map = get_search_results_map(soup)
    return [result for key in search_results_map for result in search_results_map[key]]


if __name__ == "__main__":
    import logging
    logging.basicConfig(level="DEBUG")

    from query import query_character, query_word, query_english
    from pprint import pprint
    soup = query_english("happy")
    pprint(get_search_results_map(soup))