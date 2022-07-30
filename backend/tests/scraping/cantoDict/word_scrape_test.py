# imports
from scraping.wiktionary_crawl_utils import get_soup
from scraping.cantoDict.src.scraping.entry_scraping import get_dictionary_word_summary


def test_parse_word_page_0():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/3/"
	soup = get_soup(url)
	fact = get_dictionary_word_summary(soup)

	lines = [
		"strong wind, gale"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)


def test_parse_word_page_1():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/9494/"
	assert False


def test_parse_word_page_2():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/9494/"
	assert False


def test_parse_word_page_3():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/9494/"
	assert False


def test_parse_word_page_4():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/9494/"
	assert False


def test_parse_word_page_5():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/9494/"
	assert False


def test_parse_word_page_6():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/9494/"
	assert False


def test_parse_word_page_7():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/9494/"
	assert False


def test_parse_word_page_8():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/9494/"
	assert False


def test_parse_word_page_9():
	url = "http://www.cantonese.sheik.co.uk/dictionary/words/9494/"
	assert False