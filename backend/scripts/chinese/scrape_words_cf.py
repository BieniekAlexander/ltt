'''
Collects forms from a file and publishes them to a pubsub topic for scraping
'''
import argparse
import pandas as pd
from google.cloud import pubsub
import json

# constants
language = "chinese"
PROJECT_ID = "language-training-toolkit-dev"
PENDING_TOPIC_ID = "term-scraping-pending"
PUBLISHER_CLIENT = pubsub.PublisherClient()
PENDING_TOPIC_PATH = PUBLISHER_CLIENT.topic_path(PROJECT_ID, PENDING_TOPIC_ID)

# parse runtime args from command line
parser = argparse.ArgumentParser(description="Read forms from a CSV and publish them to a pubsub topic for scraping in cloud functions")
parser.add_argument('--path-to-csv', type=str, required=True, help="The path to the CSV from which we'll read terms")
args = parser.parse_args()

# loop over the terms, find them in the lexicon, and add them to the user's vocab
words_df = pd.read_csv(args.path_to_csv)

for word in words_df['word']:
    message = json.dumps(
        {
            'language': language,
            'form': word,
            'pos': None
        }
    )

    message_encoded = message.encode('utf-8')
    future = PUBLISHER_CLIENT.publish(PENDING_TOPIC_PATH, message_encoded)
    print(future.result())