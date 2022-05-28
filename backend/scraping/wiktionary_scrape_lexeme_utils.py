#%% imports
import requests
import sys, os
from bs4 import BeautifulSoup


from utils.function_decorators import capitalize_string_args
from scraping.scraping_errors import ScrapingFormatError, ScrapingFindError
from scraping import get_wiktionary_term_url, get_soup_from_url
from model.part_of_speech import PartOfSpeech

# constants
PARTS_OF_SPEECH = [pos.value.capitalize() for pos in PartOfSpeech]


#%% utils
# see notes in README for specifics of wiktionary HTML formatting
@capitalize_string_args
def find_language_header(soup, language):
    """
    Finds the section of a wiktionary page related to the contents of a given [language]
    """
    language_span = soup.find("span", id=language)

    if language_span:
        language_header = language_span.parent

        if language_header.name != "h2":
            query_args = {'language': language}
            raise ScrapingFormatError(soup, query_args, f'Element found as language header not an h2: {query_args}')

        return language_span.parent

    return None


@capitalize_string_args
def seek_pos_header(soup, pos, language=None):
    """
    Finds the section of a wiktionary page describing the lemma, in the given [pos] and [language]
    """
    pos_span = soup.find_next('span', text=pos)

    if pos_span is None:
        return None
    else:
        pos_header = pos_span.parent
    
        if language and not verify_language_header(pos_span, language): # verify that the entry we found is under the specified language
            return None
        if pos_header.name != "h3" and pos_header.name != "h4":
            query_args = {'pos': pos, 'language': language}
            raise ScrapingFormatError(soup, query_args, f'Element found as pos header not an h3 or h4: {query_args}')
        else:
            return pos_header


@capitalize_string_args
def seek_inflection_table(soup, pos=None, language=None):
    """
    Finds the HTML table describing the inflections for the lemma of interest, in the given [pos] and [language]
    """
    query_args = {'pos': pos, 'language': language}
    table = soup.find_next('table', {'class': 'inflection-table'})

    if not table:
        return None
    else:
        if pos and not verify_pos_header(table, pos): # verify that the entry we found is under the specified pos
            return None
        if language and not verify_language_header(table, language): # verify that the entry we found is under the specified language
            return None
        return table


@capitalize_string_args
def get_inflection_table(soup, pos, language):
    """
    Find the inflections of a word in a wiktionary webpage and serialize them into a [dict]
    """
    try: # none aware access
        lang_header = find_language_header(soup, language)
        pos_header = seek_pos_header(lang_header, pos, language)
        return seek_inflection_table(pos_header, pos, language)
    except AttributeError as e:
        return None
        


@capitalize_string_args
def seek_summary_paragraph(soup, pos=None, language=None):
    """
    Finds the paragraph in the entry summarizing the features of the lemma, in the given [pos] and [language]
    """
    query_args = {'pos': pos, 'language': language}
    summary_strong = soup.find_next('strong', {'class': 'headword'})

    if not summary_strong:
        return None
    else:
        summary_paragraph = summary_strong.parent
        
        if summary_paragraph.name != 'p':
            raise ScrapingFindError(soup, query_args, f'Found a strong element, but the parent is not a paragraph: {query_args}') 
        elif pos and not verify_pos_header(summary_strong, pos): # verify that the entry we found is under the specified pos
            return None
        elif language and not verify_language_header(summary_strong, language): # verify that the entry we found is under the specified language
            return None
        return summary_paragraph


@capitalize_string_args
def get_summary_paragraph(soup, pos, language):
    """
    Get the paragraph that summarizes this lexeme, given the [pos] and [language]
    """
    # TODO is it possible that a term in a given language has multiple sections for the same part of speech? I feel like I've seen this on wiktionary before...
    try: # null safe access
        lang_header = find_language_header(soup, language)
        pos_header = seek_pos_header(lang_header, pos, language)
        return seek_summary_paragraph(pos_header, pos, language)
    except AttributeError as e:
        return None


@capitalize_string_args
def seek_definition_list(soup, pos, language):
    """
    Finds the ol element listing definitions of the lexeme, in the given [pos] and [language]
    """
    query_args = {'pos': pos, 'language': language}
    definitions_ol = soup.find_next('ol')

    if not definitions_ol:
        raise ScrapingFindError(soup, query_args, f'Could not find a definition list for: {query_args}')
    else:
        if pos and not verify_pos_header(definitions_ol, pos): # verify that the entry we found is under the specified pos
            return None
        if language and not verify_language_header(definitions_ol, language): # verify that the entry we found is under the specified language
            return None
        return definitions_ol


@capitalize_string_args
def get_definition_ol(soup, pos, language):
    """
    Get the ol element that contains the definitions for this lexeme, given the [pos] and [language]
    """
    try: # null safe access
        lang_header = find_language_header(soup, language)
        pos_header = seek_pos_header(lang_header, pos, language)
        return seek_definition_list(pos_header, pos, language)
    except AttributeError as e:
        return None


def get_definition_strings(definition_ol):
    """
    Get a list of definitions
    """
    assert definition_ol.name == "ol", "The argument must be a [BeautifulSoup] ordered list"

    definitions = []
    definition_items = definition_ol.find_all('li', recursive=False)
    
    for item in definition_items:
        # get the base text description in this li (ignore things like synonym listings)
        definition = item.get_text().split('\n')[0]
        definitions.append(definition)

    return definitions


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
def get_page_term(soup: BeautifulSoup) -> str:
    """Gets the term being described in this webpage soup

    Args:
        soup (BeautifulSoup): a parsed wiktionary webpage

    Returns:
        str: the page's term
    """
    h1 = soup.find('h1', {'id': 'firstHeading'})
    return h1.text
    

@capitalize_string_args
def get_lemma(soup: BeautifulSoup, pos: PartOfSpeech, language: str) -> str:
    """Given a webpage [soup], [language], and [pos] for a term, find the lemma related to the term, or return None if the webpage describes the lemma

    For an entry, the first definition indicates which lemma covers this term

    example pages:
    https://en.wiktionary.org/wiki/czerwony - lexeme entry
    https://en.wiktionary.org/wiki/czerwonym - inflected form entry
    https://en.wiktionary.org/wiki/emocjonalne - inflected form that doesn't have an entry
    https://en.wiktionary.org/w/index.php?search=niemo%C5%BCliwe - inflected form search leading to lexeme page
    https://en.wiktionary.org/wiki/piekło - term that is a lemma in one part of speech, and an inflected form in another
    
    notice the identification of lemma forms with the 'form-of-definition-link' class isn't used for all languages (e.g. not in Spanish)

    Args:
        soup (BeautifulSoup): the parsed wiktionary page
        pos (PartOfSpeech): the part of speech we're looking for
        language (str): the language we're looing for

    Returns:
        str: the lemma form being described in this page
    """
    try: # null safe access - first check definition
        definition_list = get_definition_ol(soup, pos, language)
        first_definition_li = definition_list.find_next('li')
        lemma_span = first_definition_li.find_next('span', {'class': 'form-of-definition-link'})
    except AttributeError as e:
        lemma_span = None

    summary_paragraph = get_summary_paragraph(soup, pos, language)

    if lemma_span \
            and (language and verify_language_header(lemma_span, language)) \
            and (pos and verify_pos_header(lemma_span, pos)): # this page references another form as the lemma
        return lemma_span.text
    elif summary_paragraph: # this page itself contains the lemma
        summary_strong = summary_paragraph.find('strong', {'class': 'headword'})
        
        if summary_strong:
            return summary_strong.text
        else: return None
    else:
        return None 
        

def get_term_parts_of_speech(soup: BeautifulSoup, language: str):
    """
    Get the parts of speech in which a term appears in a given [language]

    Finds all part-of-speech headers in the page and returns all of the found parts of speech falling under the specified language
    """
    assert soup and language

    pos_header_tags = ['h3', 'h4']
    language_header = find_language_header(soup, language)
    parts_of_speech = set()

    if language_header == None:
        query_args = {'language': language}
        raise ScrapingFormatError(soup, query_args, f"This webpage didn't contain a section for the given language - {language}")   
    else:
        for pos_str in PARTS_OF_SPEECH:
            pos_spans = language_header.find_all_next('span', text=pos_str)
            
            for pos_span in pos_spans:
                pos_header = pos_span.parent

                if pos_header.name in pos_header_tags \
                        and  verify_language_header(pos_span, language):
                    parts_of_speech.add(pos_str)
                    break

        return list(map(lambda x: x.lower(), parts_of_speech))


#%% main
def main():
    term = "psa"
    pos = "Noun"
    language = "Polish"

    soup = get_soup_from_url(get_wiktionary_term_url(term))
    get_term_parts_of_speech(soup, language)


if __name__ == "__main__":
    main()