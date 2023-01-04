import requests
from bs4 import BeautifulSoup
api_url = ' http://www.cantonese.sheik.co.uk/scripts/wordsearch.php?level=0'
headers_str = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\nAccept-Language: en,pl-PL;q=0.9,pl;q=0.8\nCache-Control: max-age=0\nConnection: keep-alive\nContent-Type: application/x-www-form-urlencoded\nDNT: 1\nOrigin: http://www.cantonese.sheik.co.uk\nReferer: http://www.cantonese.sheik.co.uk/scripts/wordsearch.php?level=0\nUpgrade-Insecure-Requests: 1\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
headers = dict(
        (tuple(map(lambda x: x.strip(), line.split(':', maxsplit=1)))
        for line in headers_str.split('\n'))
    )

def query(query_str: str, search_type: int):
    """
    TODO
    """
    data = f"TEXT={query_str}&SEARCHTYPE={search_type}&radicaldropdown=0&searchsubmit=search"
    return BeautifulSoup(requests.post(api_url, data=data.encode('utf-8'), headers=headers).text, 'lxml')

# reference: on the site: run a search, navigate to "inspect element", and inspect the payload of the network request - http://www.cantonese.sheik.co.uk/
def query_jyutping(query_str: str): return query(query_str, 3)
def query_english(query_str: str): return query(query_str, 4)
def query_character(query_str: str): return query(query_str, 2)
def query_word(query_str: str): return query(query_str, 1)

if __name__ == "__main__":
    soup = query_word("己")
    # with open('out.html', 'w') as file: TODO remove
    #     file.write(str(soup))