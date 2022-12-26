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

    stroke count unknown: http://www.cantonese.sheik.co.uk/dictionary/characters/8999/
    """
    with open('/home/alex/out.html', mode='wt', encoding='utf-8') as file:
        file.write(str(soup))
    
    character = soup.find(class_='word script').text

    word_meaning_td = soup.find(class_='wordmeaning')
    word_meaning_child_strings = word_meaning_td.text.split('\n')
    is_definition_string = lambda s: re.match('\\s*([A-Za-z]|\\[\\d+\\]).*', s) and not any((s.startswith(header) for header in ('Stroke count:',
                                                                                            'Level:',
                                                                                            'Radical:')))
    i0 = next((i for i, s in list(enumerate(word_meaning_child_strings)) if is_definition_string(s)))
    i1 = next((i for i, s in list(enumerate(word_meaning_child_strings[i0:])) if not is_definition_string(s))) + i0
    definitions = [line.strip() for line in word_meaning_child_strings[i0:i1]]
    
    radical_text_div = soup.find(class_="charradical")
    radicals = list(re.sub(r'[^\u4e00-\u9fff]', '', radical_text_div.text)) if radical_text_div is not None else []

    is_radical = (character in radicals)
    
    stroke_count_div = soup.find(class_='charstrokecount')
    if stroke_count_div is not None:
        stroke_count_text = stroke_count_div.text.split(' ')[-1]
        stroke_count = int(stroke_count_text) if stroke_count_text.isdigit() else -1
    
    word_meaning_child_strings = word_meaning_td.text.split('\n')
    is_definition_string = lambda s: re.match('\\s*([A-Za-z]|\\[\\d+\\]).*', s) and not any((s.startswith(header) for header in ('Stroke count:',
                                                                                            'Level:',
                                                                                            'Radical:')))
    i0 = next((i for i, s in list(enumerate(word_meaning_child_strings)) if is_definition_string(s)))
    i1 = next((i for i, s in list(enumerate(word_meaning_child_strings[i0:])) if not is_definition_string(s))) + i0
    definitions = [line.strip() for line in word_meaning_child_strings[i0:i1]]

    return {
        'character': character,
        'definitions':definitions,
        'radicals': radicals, # TODO cantodict seems to only have one radical, even if the char has more
        'is_radical': is_radical,
        'romanizations': {
            'jyutping':soup.find(class_='cardjyutping').text.split(' ')[0],
            'pinyin':soup.find(class_='cardpinyin').text.split(' ')[0],
        },
        'forms': {
            'traditional': character,
            'simplified': character # TODO I'm just writing this as the traditional form too - scrape the simplified form
        },
        'stroke_counts': {
            'traditional': stroke_count,
            'simplified': -1 # TODO I'm pretty sure cantodict doesn't show the counts of simplified chars
        }
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
    definition = soup.find('td', class_='wordmeaning').div.text
    return {'word':soup.find(class_='word script').text, 
     'jyutping':soup.find(class_='cardjyutping').text.split(' ')[0], 
     'definitions':[
      definition]}


def get_dictionary_example_summary(soup: BeautifulSoup):
    """
    TODO figure out definition line splitting
    TODO strip out definition parsing

    different definition representations:
    - http://www.cantonese.sheik.co.uk/dictionary/characters/152/
    - https://www.cantonese.sheik.co.uk/dictionary/characters/396/
    - http://www.cantonese.sheik.co.uk/dictionary/characters/3111/
    """
    definition = soup.find('td', class_='wordmeaning').div.text
    raise NotImplementedError('wow')
    return {'character':soup.find(class_='word script').text, 
     'jyutping':soup.find(class_='cardjyutping').text.split(' ')[0], 
     'definitions':[
      definition]}


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