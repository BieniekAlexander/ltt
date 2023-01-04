# imports
# Polish
from storage.language_datastores.polish_datastore import PolishDatastore
from storage.language_datastores.chinese_datastore import ChineseDatastore

LANGUAGE_DATASTORE_MAP = {
    "polish": PolishDatastore,
    "chinese": ChineseDatastore
}
