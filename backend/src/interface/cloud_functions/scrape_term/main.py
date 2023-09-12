import functions_framework
from scraping.wiktionary_spider import WiktionarySpider
from storage.language_datastores.polish_datastore import PolishDatastore
from storage.language_datastores.chinese_datastore import ChineseDatastore
from language.chinese.word import Word
from language.chinese.character import Character
from scraping.canto_dict import canto_dict_client
from pymongo import MongoClient
from google.cloud import pubsub
import json
from base64 import b64decode

# TODO get this connectivity URI in a more secure, parameterized way
MONGODB_URI = 'mongodb://bieniekalexander:12QwAsZx@language-training-toolk-shard-00-00.rrcr5.mongodb.net:27017,language-training-toolk-shard-00-01.rrcr5.mongodb.net:27017,language-training-toolk-shard-00-02.rrcr5.mongodb.net:27017/?ssl=true&replicaSet=atlas-9hgtjo-shard-0&authSource=admin&retryWrites=true&w=majority'
PROJECT_ID = "language-training-toolkit-dev"
FAILED_TOPIC_ID = "term-scraping-failed"
PUBLISHER_CLIENT = pubsub.PublisherClient()
FAILED_TOPIC_PATH = PUBLISHER_CLIENT.topic_path(PROJECT_ID, FAILED_TOPIC_ID)


# @functions_framework.http
# def scrape_term(request):
@functions_framework.cloud_event
def scrape_term(cloud_event):
    """
    A function wrapper to scrape terms with a cloud function.

    Args:
        request (flask.Request): The request object, which should contain a lemma, pos, and language.
    Returns:
        A dictionary representing the lexeme information.
    """
    # request_data = request.get_json()
    request_data_str = b64decode(cloud_event.data['message']['data'])
    request_data = json.loads(request_data_str)
    form = request_data['form']
    language = request_data['language']
    pos = request_data.get('pos', None)

    failure_message = str(
        {
            'request': {
                'language': language,
                'form': form,
                'pos': pos
            },
            'error': 'something went wrong'
        }
    )

    failure_message_encoded = failure_message.encode('utf-8')

    # TODO support other languages
    if language == 'polish':
        spider = WiktionarySpider()
        ds_client = MongoClient(MONGODB_URI)
        polish_datastore = PolishDatastore(ds_client)

        lexemes = polish_datastore.get_lexemes_from_form(form, language) if (not pos) \
            else [polish_datastore.get_lexemes_from_form(form, language, pos)]
        
        if lexemes != []:
            return "lexemes already in database"
        else:
            # scrape the data from the request arguments
            scraped_lexemes = spider.query_lexemes(form, language) if (not pos) \
                else [spider.query_lexeme(form, pos, language)]
    
            # if data was found for the request, add it to the database
            if scraped_lexemes != []:
                try:
                    polish_datastore.add_lexemes(scraped_lexemes)
                    return str(scraped_lexemes)
                except Exception as e:
                    return str(e)
            else:
                PUBLISHER_CLIENT.publish(FAILED_TOPIC_PATH, failure_message_encoded)
                return "done"
    elif language == 'chinese':
        # TODO make a spider thingy for cantodict too
        ds_client = MongoClient(MONGODB_URI)
        chinese_datastore = ChineseDatastore(ds_client)

        lexemes_dict = chinese_datastore.get_lexemes_from_form(form)

        if lexemes_dict != {}:
            return "lexemes already in database"
        else:
            # TODO these interfaces should be made cleaner
            # scrape the data from the request arguments
            scraped_lexeme_dict = canto_dict_client.get_fact_from_characters(form)
    
            # if data was found for the request, add it to the database
            if scraped_lexeme_dict != None:
                try:
                    if 'word' in scraped_lexeme_dict:
                        scraped_lexeme_dict['lemma'] = scraped_lexeme_dict.pop('word')
                        scraped_lexeme = Word(**scraped_lexeme_dict)
                    else:
                        scraped_lexeme_dict['lemma'] = scraped_lexeme_dict.pop('character')
                        scraped_lexeme = Character(**scraped_lexeme_dict)
                    
                    chinese_datastore.add_lexemes([scraped_lexeme])
                    return str(f"scraped lexeme from: {scraped_lexeme}")
                except Exception as e:
                    print(f"failing: {str(e)}")
                    PUBLISHER_CLIENT.publish(FAILED_TOPIC_PATH, failure_message_encoded) # TODO fill out error
                    return str(e)
            else:
                print(f"didn't find anything when scriping {form}")
                PUBLISHER_CLIENT.publish(FAILED_TOPIC_PATH, failure_message_encoded)
                return "done"
    else:
        return f"Language not supported: {language}"
