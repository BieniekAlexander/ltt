# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.9.12 (main, Apr  5 2022, 06:56:58) 
# [GCC 7.5.0]
# Embedded file name: /home/alex/projects/cobweb/examples/cantoDict/src/scraping/search_results_scraping.py
# Compiled at: 2022-07-18 14:47:35
# Size of source mod 2**32: 1671 bytes
from cgitb import text
from bs4 import BeautifulSoup
import logging

def get_results_redirect_link(soup: BeautifulSoup) -> str:
    """
    Return a redirect link from a cantodict search results page, if there exists one, otherwise return [None]
    """
    if "One character found, if your page does not redirect please" not in str(soup):
        return None

    return soup.find_all('a')[-1]['href']

def get_results_table_entries(results_table):
    results_table_rows = results_table.find_all('tr')
    header_row_index = 0
    while not results_table_rows[header_row_index].td.has_attr('width'):
        header_row_index += 1

    results = []
    for i in range(header_row_index + 1, len(results_table_rows)):
        data_row = results_table_rows[i]
        tds = data_row.find_all('td')
        url = tds[0].a['href']
        character = tds[1].span.text
        jyutping = tds[2].text
        definition = tds[4].text.strip()
        results.append({'url':url, 
         'character':character, 
         'jyutping':jyutping, 
         'definitions':[
          definition]})

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
            logging.debug('table is not a results table, skipping')

        results_table = results_table.find_next('table')

    return results_tables


def get_search_results(soup: BeautifulSoup):
    """
    Get all entries listed in the search results tables
    """
    results_tables = get_search_results_tables(soup)
    return [entry for results_table in results_tables for entry in iter((get_results_table_entries(results_table)))]
# okay decompiling __pycache__/search_results_scraping.cpython-37.pyc
