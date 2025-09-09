# web_parser.py

import os
import requests
from bs4 import BeautifulSoup

# Название канала (без @)
CHANNEL      = os.getenv('CHANNEL', 'vless_vpns')
URL          = f'https://t.me/s/{CHANNEL}'

# Сколько последних сообщений брать
FETCH_LIMIT  = int(os.getenv('FETCH_LIMIT', 2))
OUT_FILE     = 'subscribes.txt'

def fetch_messages():
    resp = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')
    # Выбираем все блоки с текстом сообщений
    text_divs = soup.select('.tgme_widget_message_text')
    # Собираем чистый текст каждого блока
    texts = [div.get_text(strip=True, separator='\n') for div in text_divs]
    # На веб-странице первые в списке — самые свежие
    return texts[:FETCH_LIMIT]

def main():
    messages = fetch_messages()
    if not messages:
        print(f'⚠️ Канал "{CHANNEL}" не вернул сообщений')
        return

    # Записываем в файл в хронологическом порядке
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        for msg in reversed(messages):
            f.write(msg + '\n')

    print(f'✅ Записано {len(messages)} сообщений в {OUT_FILE}')

if __name__ == '__main__':
    main()
