# imports
from scraping.wiktionary_crawl_utils import get_soup
from scraping.cantoDict.src.scraping.entry_scraping import get_dictionary_character_summary


def test_parse_character_page_0():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/1/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"me; my",
		"we; our; us",
		"self"
	]

	wrong = [
		"Stroke count",
		"Radical"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)


def test_parse_character_page_1():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/152/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"Stroke count",
		"Radical",
		"wind; breeze; gale",
		"news; information; rumour"
	]

	wrong = [
		"variant of 諷",
		"[粵] fung3"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)

	
def test_parse_character_page_2():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/396/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"son; child; kid; boy",
		"person; small animal, fowl or object"
	]

	wrong = [
		"Stroke count",
		"Radical",
		"close; closely-woven"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)


def test_parse_character_page_3():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/3111/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"apple"
	]

	wrong = [
		"noun",
		"Radical",
		"Stroke count: 20"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)


def test_parse_character_page_4():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/116/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"eat; have a meal",
		"food; meal; (poultry) feed",
		"sth edible; sth used for cooking",
		"eclipse"
	]

	wrong = [
		"Stroke count",
		"Radical",
		"[literary] feed"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)


def test_parse_character_page_5():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/911/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"(of moths, etc) eat into; nibble away",
		"erode; corrode",
		"eclipse"
	]

	wrong = [
		"Stroke count",
		"Radical",
		"suffer a loss; wear out"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)

def test_parse_character_page_6():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/130/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"think; consider; suppose",
		"hope; expect",
		"plan",
		"remember with longing; miss",
		"want; would like to"
	]

	wrong = [
		"Stroke count",
		"Radical",
		"Level: 1"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)

def test_parse_character_page_7():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/86/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"heart",
		"mind",
		"conscience; moral nature",
		"intention; idea; ambition; design",
		"core; middle; center; inside"

	]

	wrong = [
		"Stroke count",
		"Radical",
		"Google Frequency",
		"This term is used in both Cantonese and"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)

def test_parse_character_page_8():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/443/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"steam; vapor; gas"
	]

	wrong = [
		"Radical",
		"Stroke count: 7"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)

def test_parse_character_page_9():
	url = "http://www.cantonese.sheik.co.uk/dictionary/characters/3541/"
	soup = get_soup(url)
	fact = get_dictionary_character_summary(soup)

	lines = [
		"wok; pot; pan; boiler",
		"huge pot; cauldron"
	]

	wrong = [
		"Stroke count",
		"Radical",
		"Google Frequency"
	]

	assert any(line in definition for definition in fact['definitions'] for line in lines)
	assert all(line not in definition for definition in fact['definitions'] for line in wrong)