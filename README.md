# Introduction
I'm gonna make some scripts to help me practice language learning. There are tons of resources online for language learning, but the amount can depend on the language, so finding more, fresh practice can be hard. In this repository, I compile a Language Training Toolkit to scrape resources of information and programatically make training material.
At present, I'll be focusing on resources for Polish. While I would like to generalize, the tools will be heavily geared towards the specifics of Polish, though it might generalize to other Slavic languages. If I keep working on this toolkit, the tools provided here might end up generalizing well across other languages.


# Testing
```
pytest
```


# Roadmap
## To Do
- More extensive storage connector testing
- Storage connector exceptions
- cleaning up scraping exception
- handle connectivity issues with datastore
- handle web connectivity issues
- When I'm crawling, I'm adding the forms of a given word, and not all of the words I stumble upon - maybe I should find another way to do this?
- given annotated text, strip out words for inflection practice
- capitalized and uncapitalized forms of words

## Goals
- potentially identify classes that the verbs fit into, i.e. [conjugation groups](https://www.polishpod101.com/blog/2020/10/05/polish-conjugations/)
- Having a place to get usage data will help me crawl better, and also tell me which words are better to prioritize in terms of adding it to vocabulary and deciding how much to train it with flash cards
- generalize language model use - right now, it's basically all for Polish, what happens when I add more languages?

## Standing Questions
- I think some terms have partially completed entries, i.e. [lata](https://en.wiktionary.org/wiki/lata) - am I handling this? If I find lata, do I end up finding rok?
- How can I tailor the inflection studying to the user? I.e. can I identify what forms the user needs to study, and then give the user more of those forms?


# Useful Links
- [Python Project Structure Guide](https://docs.python-guide.org/writing/structure/)
- [Pytest Documentation](https://docs.pytest.org/en/6.2.x/)
- [CLI usage for Running tests with pytest](https://zetcode.com/python/pytest/)
- http://nkjp.pl/index.php?page=14&lang=1
- https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
- https://flask.palletsprojects.com/en/2.0.x/tutorial/views/