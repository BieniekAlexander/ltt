import functions_framework
from scraping.wiktionary_spider import WiktionarySpider

@functions_framework.http
def scrape_term(request):
    """
    A function wrapper to scrape terms with a cloud function.

    Args:
        request (flask.Request): The request object, which should contain a lemma, pos, and language.
    Returns:
        A dictionary representing the lexeme information.
    """
    request_body = request.get_json()
    term = request_body['term']
    language = request_body['language']
    pos = request_body.get('lexmee', None)

    spider = WiktionarySpider()

    if not pos:
        lexeme = spider.query_lexemes(term, language)[0]
    else:
        lexeme = spider.query_lexeme(term, pos, language)

    return lexeme.to_json()
    # TODO test and upload cloud function
    # https://realpython.com/async-io-python