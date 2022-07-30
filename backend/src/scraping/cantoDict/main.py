from bs4 import BeautifulSoup
import requests


def query(keys: dict):
    api_url = " http://www.cantonese.sheik.co.uk/scripts/wordsearch.php?level=0&TEXT=jau5&SEARCHTYPE=3&radicaldropdown=0&searchsubmit=search"
    json = {"text": "jau5"}
    response = requests.post(api_url, json)
    response.json()