from json_helper import load_json, save_json

class DataBase:
    def __init__(self, path):
        self.path = path
        self.data = load_json(f'{self.path}/data.json')
        self.parsed = load_json(f'{self.path}/parsed.json')

    def save(self):
        save_json(f'{self.path}/data.json', self.data)
        save_json(f'{self.path}/parsed.json', self.parsed)
