# Introduction
Notes on how I'm persisting lexicon and vocabulary data.

## Terminology
- Lexicon - the set of lexemes used in a given language
- Vocabulary - the set of lexemes of a Lexicon known by a given individual

## Tech Stack
MongoDB as NoSQL database

## Schema
TODO clean up this section as I go

- Lexicon:
  - _language_:
    - schema: {id, lemma, pos, ...}
    - indices:
      - {(lemma, pos), unique}
- Inflections:
  - _language_:
    - schema: {form, lexeme, pos}
    - indices:
      - {(form, pos, lexeme_id), unique}
- Vocabulary:
  - _language_:
    - schema: {user_id, lexeme_id, Stats}
    - indices:
      - {(user_id, lexeme_id), unique}

## Useful Links
[Anki's implementation of SRS and forgetting curve](https://faqs.ankiweb.net/what-spaced-repetition-algorithm.html)