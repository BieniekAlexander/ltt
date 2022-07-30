# imports
import requests
from bs4 import BeautifulSoup


# constants
api_url = " http://www.cantonese.sheik.co.uk/scripts/wordsearch.php?level=0"
headers_str = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Language: en,pl-PL;q=0.9,pl;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
DNT: 1
Origin: http://www.cantonese.sheik.co.uk
Referer: http://www.cantonese.sheik.co.uk/scripts/wordsearch.php?level=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"""

headers = dict(tuple(map(lambda x: x.strip(), line.split(':', maxsplit=1))) for line in headers_str.split('\n'))


# functions
def query_jyutping(query: str):
    """
    TODO
    """
    data = f"TEXT={query}&SEARCHTYPE=3&radicaldropdown=0&searchsubmit=search"
    return BeautifulSoup(requests.post(api_url, data=data, headers=headers).text, 'lxml')

def query_english(query: str):
    """
    TODO
    """
    data = f"TEXT={query}&SEARCHTYPE=4&radicaldropdown=0&searchsubmit=search"
    return BeautifulSoup(requests.post(api_url, data=data, headers=headers).text, 'lxml')

