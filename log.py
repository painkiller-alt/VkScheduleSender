from config import log_filename
import os
import logging
from datetime import datetime

if not os.path.exists(log_filename):  # Проверка на существование файла логов, если нет - создать
    print(f'Файл логов не найден, создаю новый: {log_filename}')
    with open(log_filename, "w", encoding='utf-8'): pass
logging.basicConfig(level=logging.INFO, filename=log_filename, encoding='utf-8')

# Логгинг
def log(text: str):
    text = f'{datetime.now().strftime("%B %d | %H:%M:%S")} --> {text}'
    print(text)
    logging.info(text)