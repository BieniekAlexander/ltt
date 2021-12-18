#%% imports
import requests
import sys, os
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.function_decorators import capitalize_string_args
from scraping.scraping_errors import ScrapingAssertionError, ScrapingFindError


#%% utils
# see notes in README for specifics of wiktionary HTML formatting
@capitalize_string_args
def find_language_header(soup, language):
    """
    Finds the section of a wiktionary page related to the contents of a given [language]
    """
    query_args = {'language': language}
    language_span = soup.find("span", id=language)

    if language_span is None:
        raise ScrapingFindError(soup, query_args, f'Could not find a wiktionary section for: {query_args}')
    else:
        language_header = language_span.parent

        if language_header.name != "h2":
            raise ScrapingAssertionError(soup, query_args, f'Element found as language header not an h2: {query_args}')

        return language_span.parent


@capitalize_string_args
def seek_pos_header(soup, pos, language=None):
    """
    Finds the section of a wiktionary page describing the lemma, in the given [pos] and [language]
    """
    query_args = {'pos': pos, 'language': language}
    pos_span = soup.find_next('span', text=pos)

    if pos_span is None:
        raise ScrapingFindError(soup, query_args, f'Could not find a wiktionary section for: {query_args}')

    pos_header = pos_span.parent
    
    if language and not verify_language_header(pos_span, language): # verify that the entry we found is under the specified language
        raise ScrapingFindError(soup, query_args, f'Could not find a wiktionary section for: {query_args}')

    if pos_header.name != "h3" and pos_header.name != "h4":
        raise ScrapingAssertionError(soup, query_args, f'Element found as pos header not an h3 or h4: {query_args}')

    return pos_header


@capitalize_string_args
def seek_inflection_table(soup, pos=None, language=None):
    """
    Finds the HTML table describing the inflections for the lemma of interest, in the given [pos] and [language]
    """
    query_args = {'pos': pos, 'language': language}
    table = soup.find_next('table', {'class': 'inflection-table'})

    if not table:
        raise ScrapingFindError(soup, query_args, f'No inflection table found: {query_args}') 
    else:
        if pos and not verify_pos_header(table, pos): # verify that the entry we found is under the specified pos
            raise ScrapingFindError(soup, query_args, f'The inflection table that we found was not under the expected pos header: {query_args}')

        if language and not verify_language_header(table, language): # verify that the entry we found is under the specified language
            raise ScrapingFindError(soup, query_args, f'The inflection table that we found was not under the expected language: {query_args}')

        return table


@capitalize_string_args
def get_inflection_table(soup, pos, language):
    """
    Find the inflections of a word in a wiktionary webpage and serialize them into a [dict]
    """
    lang_header = find_language_header(soup, language)
    pos_header = seek_pos_header(lang_header, pos, language)
    return seek_inflection_table(pos_header, pos, language)


@capitalize_string_args
def seek_summary_paragraph(soup, pos=None, language=None):
    """
    Finds the paragraph in the entry summarizing the features of the lemma, in the given [pos] and [language]
    """
    query_args = {'pos': pos, 'language': language}
    summary_strong = soup.find_next('strong', {'class': 'headword'})

    if not summary_strong:
        raise ScrapingFindError(soup, query_args, f'No summary containing the term found: {query_args}') 

    else:
        summary_paragraph = summary_strong.parent
        
        if summary_paragraph.name != 'p':
            raise ScrapingFindError(soup, query_args, f'Found a strong element, but the parent is not a paragraph: {query_args}') 

        if pos and not verify_pos_header(summary_strong, pos): # verify that the entry we found is under the specified pos
            raise ScrapingFindError(soup, query_args, f'The summary we found was not under the expected pos header: {query_args}')

        if language and not verify_language_header(summary_strong, language): # verify that the entry we found is under the specified language
            raise ScrapingFindError(soup, query_args, f'The summary that we found was not under the expected language: {query_args}')

        return summary_paragraph


@capitalize_string_args
def get_summary_paragraph(soup, pos, language):
    """
    Get the paragraph that summarizes this lexeme, given the [pos] and [language]
    """
    lang_header = find_language_header(soup, language)
    pos_header = seek_pos_header(lang_header, pos, language)
    return seek_summary_paragraph(pos_header, pos, language)


@capitalize_string_args
def seek_definition_list(soup, pos, language):
    """
    Finds the ol element listing definitions of the lexeme, in the given [pos] and [language]
    """
    query_args = {'pos': pos, 'language': language}
    definitions_ol = soup.find_next('ol')

    if definitions_ol is None:
        raise ScrapingFindError(soup, query_args, f'Could not find a definition list for: {query_args}')

    if pos and not verify_pos_header(definitions_ol, pos): # verify that the entry we found is under the specified pos
            raise ScrapingFindError(soup, query_args, f'The definition list that we found was not under the expected pos header: {query_args}')
    
    if language and not verify_language_header(definitions_ol, language): # verify that the entry we found is under the specified language
        raise ScrapingFindError(soup, query_args, f'Could not find a definition list for: {query_args}')

    return definitions_ol


@capitalize_string_args
def get_definition_list(soup, pos, language):
    """
    Get the ol element that contains the definitions for this lexeme, given the [pos] and [language]
    """
    lang_header = find_language_header(soup, language)
    pos_header = seek_pos_header(lang_header, pos, language)
    return seek_definition_list(pos_header, pos, language)


def get_definition_strings(definition_ol):
    """
    Get a list of definitions, TODO as strings, from the ordered list element 
    """
    definitions = []
    definition_items = definition_ol.find_all('li', recursive=False)
    
    for item in definition_items:
        # get the base text description in this li (ignore things like synonym listings)
        definition = item.get_text().split('\n')[0]
        definitions.append(definition)

    return definitions


def verify_language_header(soup, language):
    """
    Return True if the preceding h2 indicates the [language] that we expect

    We perform this check to avoid the situation where we've searched for a tag in a webpage, and the tag is in a different section
    """
    language_header = soup.find_previous('h2')

    if language_header and language_header.span.text == language:
        return True

    return False


@capitalize_string_args
def verify_language_header(soup, language):
    """
    Return True if the preceding h2 indicates the [language] that we expect

    We perform this check to avoid the situation where we've searched for a tag in a webpage, and the tag is in a different section
    """
    language_header = soup.find_previous('h2')
        
    if language_header and language_header.span.text != language:
        return False

    return True


@capitalize_string_args
def verify_pos_header(soup, pos):
    """
    Return True if the preceding h3 or h4 indicates the [pos] that we expect

    We perform this check to avoid the situation where we've searched for a tag in a webpage, and the tag is in a different section
    """
    pos_header = soup.find_previous('h3')

    if pos_header and pos_header.span.text == pos:
        return True

    pos_header = soup.find_previous('h4')

    if pos_header and pos_header.span.text == pos:
        return True

    return False


@capitalize_string_args
def get_lemma(soup, pos, language):
    """
    Given a webpage [soup], [language], and [pos] for a term, find the lemma related to the term, or return None if the webpage describes the lemma

    For an entry, the first definition indicates which lemma covers this term
    """
    # notice the identification of lemma forms with the 'form-of-definition-link' class isn't used for all languages (e.g. not in Spanish)
    definition_list = get_definition_list(soup, pos, language)
    first_definition = definition_list.find_next('li')
    lemma_span = first_definition.find_next('span', {'class': 'form-of-definition-link'})
    print(lemma_span)

    if lemma_span: # we've identified the lemma (make sure of it), return it
        if (language and not verify_language_header(lemma_span, language))\
                or (language and not verify_pos_header(lemma_span, pos)):
            return None
        else:
            return lemma_span.text
    else: # we found no lemma form, so this term is probably the lemma - return None to indicate that
        return None


#%% main
def main():
    lemma = "psa"
    pos = "Noun"
    language = "Polish"

    termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
    page = requests.get(termUrl)
    soup = BeautifulSoup(page.content, "html.parser")
    lemma = get_lemma(soup, pos, language)
    print(lemma)


if __name__ == "__main__":
    main()