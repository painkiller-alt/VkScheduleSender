from json_helper import load_json, save_json
from pymongo.mongo_client import MongoClient
from pymongo import collection
from config import mongodb_uri, test

class DataBase:
    def __init__(self, path):
        self.path = path
        self.data = load_json(f'{self.path}/data.json')
        self.parsed = load_json(f'{self.path}/parsed.json')

        self.client = MongoClient(mongodb_uri)

        if test:
            self._db = self.client.KTCbot_data_test
        else:
            self._db = self.client.KTCbot_data

        self.colleges: collection.Collection = self._db.colleges

    def save(self):
        save_json(f'{self.path}/data.json', self.data)
        save_json(f'{self.path}/parsed.json', self.parsed)

    def push_images(self, coll_name: str, images: dict):
        self.colleges[coll_name]