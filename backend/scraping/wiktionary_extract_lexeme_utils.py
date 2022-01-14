#%% imports
import sys, os, requests, re, logging, json
from bs4 import BeautifulSoup, Tag

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.inflected_lexeme import InflectedLexeme
from scraping.wiktionary_scrape_lexeme_utils import get_inflection_table, get_summary_paragraph, get_definition_ol, get_definition_strings
from scraping.html_parse_utils import parse_inflection_table
from scraping.scraping_errors import ScrapingFindError, ScrapingValueError
from model.lexeme import LexemeEncoder
from model import model_class_map
from model.polish.feat.case import Case


#%% utils
def extract_lexeme(soup, lemma, pos, language):
  """
  Extract the information from the [soup] webpage for the given [lemma], [pos], and [language] and returns it in a model object
  """
  model_class = model_class_map[language.upper()][pos.upper()]
  kwargs = {}
  
  if issubclass(model_class, InflectedLexeme):
    inflection_table = get_inflection_table(soup, pos, language)
    inflection_dict = parse_inflection_table(inflection_table)
    kwargs['inflections'] = inflection_dict

  if pos.lower() == "adjective":
    adjective_summary = parse_features_adjective(soup, pos, language)
    kwargs.update(adjective_summary)
  elif pos.lower() == "adverb":
    adverb_summary = parse_features_adverb(soup, pos, language)
    kwargs.update(adverb_summary)
  elif pos.lower() == "noun":
    noun_summary = parse_features_noun(soup, pos, language)
    kwargs.update(noun_summary)
  elif pos.lower() == "verb":
    verb_summary = parse_features_verb(soup, pos, language)
    kwargs.update(verb_summary)
  elif pos.lower() == "preposition":
    conjunction_summary = parse_features_conjunction(soup, pos, language)
    kwargs.update(conjunction_summary)
  elif pos.lower() == "conjunction" \
      or pos.lower() == "interjection" \
      or pos.lower() == "numeral" \
      or pos.lower() == "particle" \
      or pos.lower() == "pronoun":
    pass # no features to parse
  else:
    raise ValueError(f"Tried to extract an unknown part of speech: {pos.lower()}")

  definition_list = get_definition_ol(soup, pos, language)
  definitions = get_definition_strings(definition_list)

  lexeme = model_class(lemma, pos, definitions, **kwargs)
  return lexeme


def parse_features_noun(soup, pos, language):
  """
  Reads the [soup] of the webpage, searching for the lexeme in the particular [langauge] and [pos], and collects the features of the noun it describes

  sample summary string: "kot m anim (diminutive kotek or koteczek, augmentative kocur, feminine kocica or kotka)"
  """
  lemma_summary_paragraph = get_summary_paragraph(soup, pos, language)
  summary_string = lemma_summary_paragraph.get_text()
  definition_list = get_definition_ol(soup, pos, language)
  definitions = get_definition_strings(definition_list)
  ret = {}

  # get gender information
  gender_span = lemma_summary_paragraph.find_next('span', {'class': 'gender'})
  
  if not gender_span:
    raise ScrapingFindError(lemma_summary_paragraph, {}, "Could not find gender information for this noun")
  else:
    for abbr in gender_span.find_all("abbr"):
      value = abbr['title']

      if value == 'nonvirile':
        ret['virility'] = 'nonvirile'
      elif value == 'nonvirile':
        ret['virility'] = 'nonvirile'
      elif value == 'masculine gender':
        ret['gender'] = 'male'
      elif value == 'feminine gender':
        ret['gender'] = 'female'
      elif value == 'neuter gender':
        ret['gender'] = 'neuter'
      elif value == 'animate':
        ret['animacy'] = 'animate'
      elif value == 'inanimate':
        ret['animacy'] = 'inanimate'
      elif value in ['personal', 'plural number']: # skipping parsing, ludzie, człowiek
        logging.warn(f"skipping parsing of noun data for gender={value}")
      else:
        query_args = {'pos': pos, 'language': language}
        raise ScrapingValueError(gender_span, query_args, 'gender', value)

  # get diminutive, augmentative, male, female forms
  forms_match = re.search(r'\(.*\)', summary_string)
  forms = ['diminutive', 'augmentative', 'masculine', 'feminine']

  if forms_match:
    forms_string = forms_match.group(0)[1:-1]
    sections = list(map(lambda x: x.strip(), forms_string.split(',')))
    
    for section in sections:
      for form in forms: # check the section for form labels and parse out the forms
        if form in section:
          entries_string = section.replace(form, "")
          entry_strings = re.split(r' or |,', entries_string) # split out entries
          entries_raw = list(filter(lambda x: x.strip() != '', entry_strings)) # remove empty strings
          entries = list(map(lambda x: x.strip(), entries_raw)) # clean entry strings
          ret[form] = entries
          break
      else:
        query_args = {'pos': pos, 'language': language}
        raise ScrapingValueError(lemma_summary_paragraph, query_args, None, None, "This noun summary section contained a property that we're not accounting for")
      
  return ret


def parse_features_verb(soup, pos, language):
  """
  Reads the [soup] of the webpage, searching for the lexeme in the particular [langauge] and [pos], and collects the features of the verb it describes

  sample summary string: "biec impf (determinate, perfective pobiec, indeterminate biegać)"
  """
  lemma_summary_paragraph = get_summary_paragraph(soup, pos, language)
  summary_string = lemma_summary_paragraph.get_text()
  definition_list = get_definition_ol(soup, pos, language)
  definitions = get_definition_strings(definition_list)
  ret = {}

  # get aspect information
  aspect_span = lemma_summary_paragraph.find_next('span', {'class': 'gender'}) # html seems mislabeled, notice class=gender
  
  if not aspect_span:
    raise ScrapingFindError(lemma_summary_paragraph, {}, "Could not find aspect information for this verb")
  else:
    for abbr in aspect_span.find_all("abbr"):
      value = abbr['title']

      if value == 'imperfective aspect':
        ret['aspect'] = 'imperfect'
      elif value == 'perfective aspect':
        ret['aspect'] = 'perfect'
      else:
        query_args = {'pos': pos, 'language': language}
        raise ScrapingValueError(aspect_span, query_args, 'aspect', value)

  # get abstraction, alternate forms
  forms_match = re.search(r'\(.*\)', summary_string)
  forms = ['perfective', 'imperfective', 'indeterminate', 'imperfective determinate', 'frequentative', 'determinate', '+']

  if forms_match:
    forms_string = forms_match.group(0)[1:-1]
    sections = list(map(lambda x: x.strip(), forms_string.split(',')))

    for section in sections:
      for form in forms: # check the section for form labels and parse out the forms
        if form in section:
          entries_string = section.replace(form, "")

          if form == '+': # TODO some verb sections describe associated cases, skipping this for now
            logging.warn(f"Skpping parsing of this verb case usage summary section - {section}") 

          if entries_string.strip() == "": # this section describes a property of this verb (e.g. "frequentative")
            if form == "perfective":
              ret['aspect'] = "perfect"
            elif form == "imperfective":
              ret['aspect'] = "imperfect"
            elif form == "indeterminate":
              ret['abstraction'] = "indeterminate"
            elif form == "determinate":
              ret['abstraction'] = "determinate"
            elif form == "imperfective determinate":
              ret['aspect'] = "imperfect"
              ret['abstraction'] = "determinate"
            elif form == "frequentative":
              ret['is_frequentative'] = True

          else: # this section describes alternative forms (e.g. "perfective zjeść")
            entry_strings = re.split(r' or |,', entries_string) # split out entries
            entries_raw = list(filter(lambda x: x.strip() != '', entry_strings)) # remove empty strings
            entries = list(map(lambda x: x.strip(), entries_raw)) # clean entry strings
            ret[form] = entries

          break
    
      else:
        query_args = {'pos': pos, 'language': language}
        raise ScrapingValueError(lemma_summary_paragraph, query_args, None, section, f"This verb summary section contained a property that we're not accounting for - {section}")
      
  return ret


def parse_features_adjective(soup, pos, language):
  """
  Reads the [soup] of the webpage, searching for the lexeme in the particular [langauge] and [pos], and collects the features of the adjective it describes

  sample summary strings:
  - "czerwony (comparative czerwieńszy or bardziej czerwony, superlative najczerwieńszy or najbardziej czerwony, adverb czerwono)"
  - "czerwonawy (not comparable, adverb czarwonawo)"
  """
  lemma_summary_paragraph = get_summary_paragraph(soup, pos, language)
  summary_string = lemma_summary_paragraph.get_text()
  definition_list = get_definition_ol(soup, pos, language)
  definitions = get_definition_strings(definition_list)
  ret = {}

  # get alternate forms
  forms_match = re.search(r'\(.*\)', summary_string)
  forms = ['comparative', 'superlative', 'adverb', 'not comparable']

  if forms_match: # if the adjective describes other forms (or lack thereof), it's usually the positive form
    ret['degree'] = 'positive'
    forms_string = forms_match.group(0)[1:-1]
    sections = list(map(lambda x: x.strip(), forms_string.split(',')))

    for section in sections:
      for form in forms: # check the section for form labels and parse out the forms
        if form in section:
          entries_string = section.replace(form, "")

          if entries_string.strip() in ['not always comparable']: # skipping weird edge cases in the summary section
            pass
          elif entries_string.strip() == "" and form != "not comparable":
            query_args = {'pos': pos, 'language': language}
            raise ScrapingValueError(lemma_summary_paragraph, query_args, None, section, f"This adjective summary section contained a property that we're not accounting for - {section}")
          elif form == "not comparable":
            ret['not_comparable'] = True
          else: # this section describes alternative forms (e.g. "comparative czerwieńszy or bardziej czerwony")
            entry_strings = re.split(r' or |,', entries_string) # split out entries
            entries_raw = list(filter(lambda x: x.strip() != '', entry_strings)) # remove empty strings
            entries = list(map(lambda x: x.strip(), entries_raw)) # clean entry strings
            ret[form] = entries

          break
    
      else:
        query_args = {'pos': pos, 'language': language}
        raise ScrapingValueError(lemma_summary_paragraph, query_args, None, section, f"This adjective summary section contained a property that we're not accounting for - {section}")

  else: # the comparative and superlative entries don't have summaries - they instead list degree in the definition (e.g. "comparative degree of czerwony")
    # https://stackoverflow.com/a/42536557
    degree_definition = definitions[0]

    if 'comparative degree' in degree_definition:
      positive = re.match(r'comparative degree of ([a-zA-Z]*)', degree_definition).group(1)
      ret['degree'] = 'comparative'
      ret['positive'] = [positive]
    elif 'superlative degree' in degree_definition:
      positive = re.match(r'superlative degree of ([a-zA-Z]*)', degree_definition).group(1)
      ret['degree'] = 'superlative'
      ret['positive'] = [positive]
    else:
      args = {'pos': pos, 'language': language}
      raise ScrapingFindError(soup, args, "Expected description of non-positive degreed adjective, failed to parse such information")

  return ret


def parse_features_adverb(soup, pos, language):
  """
  Reads the [soup] of the webpage, searching for the lexeme in the particular [langauge] and [pos], and collects the features of the adverb it describes

  sample summary strings:
  - mało (not comparable)
  """
  lemma_summary_paragraph = get_summary_paragraph(soup, pos, language)
  summary_string = lemma_summary_paragraph.get_text()
  definition_list = get_definition_ol(soup, pos, language)
  definitions = get_definition_strings(definition_list)
  ret = {}

  # get alternate forms
  forms_match = re.search(r'\(.*\)', summary_string)
  forms = ['comparative', 'superlative', 'adjective', 'not comparable']

  if forms_match: # if the adverb describes other forms (or lack thereof), it's usually the positive form
    ret['degree'] = 'positive'
    forms_string = forms_match.group(0)[1:-1]
    sections = list(map(lambda x: x.strip(), forms_string.split(',')))

    for section in sections:
      for form in forms: # check the section for form labels and parse out the forms
        if form in section:
          entries_string = section.replace(form, "")

          if entries_string.strip() == "" and form != "not comparable":
            query_args = {'pos': pos, 'language': language}
            raise ScrapingValueError(lemma_summary_paragraph, query_args, None, section, f"This adverb summary section contained a property that we're not accounting for - {section}")
          elif form == "not comparable":
            ret['not_comparable'] = True
          else: # this section describes alternative forms (e.g. "comparative czerwieńszy or bardziej czerwony")
            entry_strings = re.split(r' or |,', entries_string) # split out entries
            entries_raw = list(filter(lambda x: x.strip() != '', entry_strings)) # remove empty strings
            entries = list(map(lambda x: x.strip(), entries_raw)) # clean entry strings
            ret[form] = entries

          break
    
      else:
        query_args = {'pos': pos, 'language': language}
        raise ScrapingValueError(lemma_summary_paragraph, query_args, None, section, f"This adverb summary section contained a property that we're not accounting for - {section}")

  else: # the comparative and superlative entries don't have summaries - they instead list degree in the definition (e.g. "comparative degree of szybko")
    # https://stackoverflow.com/a/42536557
    degree_definition = definitions[0]

    if 'comparative degree' in degree_definition:
      positive = re.match(r'comparative degree of ([a-zA-Z]*)', degree_definition).group(1)
      ret['degree'] = 'comparative'
      ret['positive'] = [positive]
    elif 'superlative degree' in degree_definition:
      positive = re.match(r'superlative degree of ([a-zA-Z]*)', degree_definition).group(1)
      ret['degree'] = 'superlative'
      ret['positive'] = [positive]
    else:
      args = {'pos': pos, 'language': language}
      raise ScrapingFindError(soup, args, "Expected description of non-positive degreed adjective, failed to parse such information")

  return ret


def parse_features_conjunction(soup, pos, language):
  """
  Reads the [soup] of the webpage, searching for the lexeme in the particular [langauge] and [pos], and collects the features of the adverb it describes

  sample summary strings:
  - mało (not comparable)
  """
  lemma_summary_paragraph = get_summary_paragraph(soup, pos, language)
  summary_string = lemma_summary_paragraph.get_text()
  definition_list = get_definition_ol(soup, pos, language)
  definitions = get_definition_strings(definition_list)
  ret = {'cases': set()}

  # check if the summary string has any information about cases
  match = re.match(r'.*\(\+ (.*)\)', summary_string)

  if match:
    ret['cases'].add(match.group(1))

  for definition in definitions:
    for case in list(map(lambda x: x.lower(), [c.name for c in Case])):
      if case in definition:
        ret['cases'].add(case)

  ret['cases'] = list(ret['cases'])
  return ret


#%% main
def main():
  lemma, pos, language = "czerwony", "Noun", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  ret = extract_lexeme(soup, lemma, pos, language)
  json_str = json.dumps(ret, cls=LexemeEncoder)
  print(json_str)


if __name__ == "__main__":
    main()