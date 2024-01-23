import os
import json

# Загрузка данных из json
def load_json(filename: str, create_new: bool=True, not_found_error=False):
    if os.path.exists(filename):
        with open(filename, "r", encoding='utf-8') as load_file:
            if load_file.read() != '':
                load_file.seek(0) # После чтения файла (в условии) нужно переместить ползунок снова в начало
                return json.load(load_file)
            else:
                if not_found_error:
                    print(f'{filename} пустой')
                return {}
    else:
        if not_found_error:
            print(f'{filename} не найден')
            raise ValueError
        if create_new:
            print(f'{filename} не найден, создаю новый')
            with open(filename, "w", encoding='utf-8'):
                pass
        return {}

# Сохранение json
def save_json(filename: str, obj):
    with open(filename, 'w', encoding='utf-8') as save_file:
        json.dump(obj, save_file, indent=4, ensure_ascii=False)