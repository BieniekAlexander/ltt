# Introduction
Notes on how I'm persisting lexicon and vocabulary data.

## Terminology
- Lexicon - the set of lexemes used in a given language
- Vocabulary - the set of lexemes of a Lexicon known by a given individual

## Schema
- Lexicon:
  - _language_:
    - {id, lexeme, pos, ...}
- Vocabulary:
  - _language_:
    - {user, id, rating, ...}