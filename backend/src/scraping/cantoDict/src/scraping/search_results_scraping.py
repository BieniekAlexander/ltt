from cgitb import text
from bs4 import BeautifulSoup
import logging


def get_results_table_entries(results_table):
    results_table_rows = results_table.find_all('tr')
    header_row_index = 0 # the header row will have a "width" field in the first td
    while not results_table_rows[header_row_index].td.has_attr('width'):
        header_row_index += 1

    results = []
    for i in range(header_row_index+1, len(results_table_rows)):
        data_row = results_table_rows[i]
        tds = data_row.find_all("td")
        url = tds[0].a['href']
        character = tds[1].span.text
        jyutping = tds[2].text
        definition = tds[4].text.strip()

        results.append({
                'url': url,
                'character': character,
                'jyutping': jyutping,
                'definitions': [definition]
                })

    return results

def get_search_results_tables(soup: BeautifulSoup):
    """
    Get each BeautifulSoup table containing vocabulary entries
    """
    results_tables = []
    results_table = soup.find('table')

    while results_table:
        try:
            if 'entries for' in results_table.tr.td.b.text:
                results_tables.append(results_table)
        except:
            logging.debug("table is not a results table, skipping")

        results_table = results_table.find_next('table')

    return(results_tables)

def get_search_results(soup: BeautifulSoup):
    """
    Get all entries listed in the search results tables
    """
    results_tables = get_search_results_tables(soup)
    return [entry for results_table in results_tables for entry in get_results_table_entries(results_table)]