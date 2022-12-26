# %% imports
import requests
from bs4 import BeautifulSoup
from utils.function_decorators import delay


# %% utils
def get_wiktionary_term_url(
    term): return f"https://en.wiktionary.org/wiki/{term}"


def get_wiktionary_search_url(
    term): return f"https://en.wiktionary.org/w/index.php?search={term}&title=Special:Search&profile=advanced&fulltext=1&searchengineselect=mediawiki&ns0=1"
# TODO the URL is sometimes redirecting, I'm using all of the URL arguments to force this behavior, how do I do this more nicely?
# "https://en.wiktionary.org/w/index.php?search={term}"


@delay(1)
def get_soup_from_url(url: str):
    """
    Helper function to get the [BeautifulSoup] object from a URL 
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
