# Introduction
This section documents implementation of the Chinese language in this project. Given the homogenous written and different spoken forms, I'll store all chinese lemmas together in an object that represents their written form, and I'll track information regarding dialects within that object.

## references:
- [Chinese Part of Speech Reference]([http://tecfaetu.unige.ch/staf/staf-e/sun/staf15/cgrammar/cgrammer.html)
- [Traditional vs Simplified Characters](https://eriksen.com/language/simplified-vs-traditional-chinese)
  - According to this, traditional to simplified is many to one, so I'll use the traditional form as the lemma form of the word