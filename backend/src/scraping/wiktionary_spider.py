import logging

import requests
from bs4 import BeautifulSoup
from scraping import (get_soup_from_url, get_wiktionary_search_url,
                      get_wiktionary_term_url)
from scraping.wiktionary_crawl_utils import (get_search_result_links,
                                             is_entries_page,
                                             is_no_entries_page,
                                             is_search_results_page)
from scraping.wiktionary_extract_lexeme_utils import extract_lexeme
from scraping.wiktionary_scrape_lexeme_utils import (find_language_header,
                                                     get_lemma, get_page_term,
                                                     get_term_parts_of_speech)


class WiktionarySpider(object):
    """Object for managing the acquiring of data from wiktionary."""

    def __init__(self):
        """Constructor"""
        self.steps = []

    def step(self, url: str) -> BeautifulSoup:
        """Go to the next webpage and add the webpage to the call stack

        Args:
            url (str): the next url that the spider is visiting

        Returns:
            BeautifulSoup: a beautifulsoup object to parse
        """
        assert isinstance(url, str)

        self.steps.append(url)
        return get_soup_from_url(url)

    # TODO the two query functions have duplicate code, I wonder if I can merge them nicely

    def query_lexeme(self, term: str, pos: str, language: str, max_step_count: int = 5):
        """Runs a DFS to get the lexeme described by the arguments

        Args:
            term (str): [description]
            pos (str): the part of speech we want
            language (str): [description]
            depth (int): The maximum number of steps to take when looking for the lexeme

        Returns:
            [type]: [description]
        """
        assert isinstance(language, str)
        assert isinstance(term, str)
        assert isinstance(max_step_count, int)

        pos = pos.lower()
        url_stack = [get_wiktionary_term_url(term)]
        steps_left = max_step_count

        while url_stack and steps_left > 0:
            url = url_stack.pop()
            soup = self.step(url)

            # this page doesn't have any entries, jump to the search page (we'll probably only hit this once?)
            if is_no_entries_page(soup):
                url_stack.append(get_wiktionary_search_url(term))
                logging.info(f"Found no entries on this page - {url}")

            elif is_search_results_page(soup):
                search_result_links = get_search_result_links(soup)
                search_result_links.reverse()
                print(search_result_links)
                url_stack = search_result_links + url_stack

            elif is_entries_page(soup):  # if the page has entries, process them
                if not find_language_header(soup, language):
                    continue

                page_term = get_page_term(soup)
                parts_of_speech = get_term_parts_of_speech(soup, language)

                if pos in parts_of_speech:  # only get a result for the part of speech we're interested in
                    lemma = get_lemma(soup, pos, language)

                    if page_term == lemma:  # our lexeme is on this page
                        result = extract_lexeme(soup, lemma, pos, language)
                        return result

                    else:  # our lexeme is not on this page, let's go to the page for the lemma described
                        url_stack.append(get_wiktionary_term_url(lemma))

            steps_left -= 1

        return None

    def query_lexemes(self, term, language, max_step_count: int = 5):
        """Runs a DFS to get the lexemes described by the arguments

        Args:
            language (str): [description]
            term (type): [description]
            depth (int): The maximum number of steps to take when looking for the lexeme

        Returns:
            [type]: [description]
        """
        assert isinstance(language, str)
        assert isinstance(term, str)
        assert isinstance(max_step_count, int)

        url_stack = [get_wiktionary_term_url(term)]
        steps_left = max_step_count
        results = []

        while url_stack and steps_left > 0:
            url = url_stack.pop()
            soup = self.step(url)

            # this page doesn't have any entries, jump to the search page (we'll probably only hit this once?)
            if is_no_entries_page(soup):
                url_stack.append(get_wiktionary_search_url(term))
                logging.info(f"Found no entries on this page - {url}")

            elif is_search_results_page(soup):
                search_result_links = get_search_result_links(soup)
                search_result_links.reverse()
                url_stack = search_result_links + url_stack

            elif is_entries_page(soup):  # if the page has entries, process them
                if not find_language_header(soup, language):
                    continue

                page_term = get_page_term(soup)
                parts_of_speech = get_term_parts_of_speech(soup, language)

                for pos in parts_of_speech:
                    lemma = get_lemma(soup, pos, language)

                    if page_term == lemma:  # our lexeme is on this page
                        result = extract_lexeme(soup, lemma, pos, language)

                        if all(result != r for r in results):  # ignore duplicate entries
                            results.append(result)

                    else:  # our lexeme is not on this page, let's go to the page for the lemma described
                        url = get_wiktionary_term_url(lemma)

                        if url not in self.steps and url not in url_stack:
                            url_stack.append(get_wiktionary_term_url(lemma))

            steps_left -= 1

        return results


def main():
    # spider = WiktionarySpider()
    # result = spider.query_lexeme('zimna', 'noun', 'polish')
    # print(result.to_json())

    spider = WiktionarySpider()
    results = spider.query_lexemes('piekło', 'polish')

    for r in results:
        print(r.to_json_dictionary)


if __name__ == "__main__":
    main()
