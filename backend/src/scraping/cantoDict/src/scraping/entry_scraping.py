from bs4 import BeautifulSoup
import re


def get_dictionary_character_summary(soup: BeautifulSoup):
    """
    TODO figure out definition line splitting
    TODO strip out definition parsing

    different definition representations:
    - http://www.cantonese.sheik.co.uk/dictionary/characters/152/
    - https://www.cantonese.sheik.co.uk/dictionary/characters/396/
    - http://www.cantonese.sheik.co.uk/dictionary/characters/3111/
    """
    word_meaning_td = soup.find(class_="wordmeaning")
    word_meaning_child_strings = word_meaning_td.text.split('\n')
    
    is_definition_string = lambda s: re.match("\s*([A-Za-z]|\[\d+\]).*", s) and not any(s.startswith(header) for header in ['Stroke count:', 'Level:', "Radical:"])
    i0 = next(i for i, s in list(enumerate(word_meaning_child_strings)) if is_definition_string(s))
    i1 = next(i for i, s in list(enumerate(word_meaning_child_strings[i0:])) if not is_definition_string(s)) + i0
    definitions = [line.strip() for line in word_meaning_child_strings[i0:i1]]

    return {
        'character': soup.find(class_="word script").text,
        'jyutping': soup.find(class_="cardjyutping").text.split(' ')[0],
        'definitions': definitions
    }

def get_dictionary_word_summary(soup: BeautifulSoup):
    """
    TODO figure out definition line splitting
    TODO strip out definition parsing

    different definition representations:
    - http://www.cantonese.sheik.co.uk/dictionary/words/3/
    - http://www.cantonese.sheik.co.uk/dictionary/words/9494/
    - http://www.cantonese.sheik.co.uk/dictionary/characters/3111/
    """
    definition = soup.find('td', class_="wordmeaning").div.text

    return {
        'word': soup.find(class_="word script").text,
        'jyutping': soup.find(class_="cardjyutping").text.split(' ')[0],
        'definitions': [definition]
    }

def get_dictionary_example_summary(soup: BeautifulSoup):
    """
    TODO figure out definition line splitting
    TODO strip out definition parsing

    different definition representations:
    - http://www.cantonese.sheik.co.uk/dictionary/characters/152/
    - https://www.cantonese.sheik.co.uk/dictionary/characters/396/
    - http://www.cantonese.sheik.co.uk/dictionary/characters/3111/
    """
    definition = soup.find('td', class_="wordmeaning").div.text
    raise NotImplementedError("wow")

    return {
        'character': soup.find(class_="word script").text,
        'jyutping': soup.find(class_="cardjyutping").text.split(' ')[0],
        'definitions': [definition]
    }

def get_dictionary_word_characters(soup: BeautifulSoup):
    """
    TODO
    """
    raise NotImplementedError()

def get_dictionary_word_compound_words(soup: BeautifulSoup):
    """
    TODO
    """
    raise NotImplementedError()
    
def get_dictionary_word_examples(soup: BeautifulSoup):
    """
    TODO
    """
    raise NotImplementedError()
    
def get_dictionary_character_words(soup: BeautifulSoup):
    """
    TODO
    """
    raise NotImplementedError()

def get_dictionary_character_examples(soup: BeautifulSoup):
    """
    TODO
    """
    raise NotImplementedError()

def get_dictionary_example_words(soup: BeautifulSoup):
    """
    TODO
    """
    raise NotImplementedError()