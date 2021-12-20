# Introduction
Use these modules to scrape the internet for language data. Curently, all of the scraping utilities are made for wiktionary.org.


# Website Scraping Notes
## Wiktionary.org
- Formattings actually differ across languages (and even within languages) - as of now, my notes will largely describe polish entries
- headers
  - h1 headers - title of entry
  - h2 headers - lemma's language entries
  - h3/h4 headers - lemma's entry, for a given part of speech, under a given language (usually h3)
- URLs
  - entry page link format: https://en.wiktionary.org/wiki/\<term\>
  - search page format: https://en.wiktionary.org/w/index.php?search=\<term\>


# Useful Links


# Known Issues
Some pages seem to be malformed:
- https://en.wiktionary.org/wiki/lecz - Conjunction section is h4, should be h3
- https://en.wiktionary.org/wiki/a#Polish - seems to have a ton of memory errors in the webpage
- https://en.wiktionary.org/wiki/chodzi%C4%87#Polish - some verbs seem to be missing abstraction (i.e. chodzić is indeterminate)