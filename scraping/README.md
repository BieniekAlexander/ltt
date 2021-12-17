# Introduction
Use these modules to scrape the internet for language data. Curently, all of the scraping utilities are made for wiktionary.org.


# Website Scraping Notes
## Wiktionary.org
### HTML formatting
- h1 headers - title of entry
- h2 headers - lemma's language entries
- h3 headers - lemma's entry, for a given part of speech, under a given language (sometimes h4 though?)


# Useful Links


# Known Issues
Some pages seem to be malformed:
- https://en.wiktionary.org/wiki/lecz - Conjunction section is h4, should be h3
- https://en.wiktionary.org/wiki/a#Polish - seems to have a ton of memory errors in the webpage
- https://en.wiktionary.org/wiki/chodzi%C4%87#Polish - some verbs seem to be missing abstraction (i.e. chodzić is indeterminate)