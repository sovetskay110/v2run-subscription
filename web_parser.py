# web_parser.py

import os
import requests
from bs4 import BeautifulSoup

# Название канала (без @)
CHANNEL    = os.getenv('CHANNEL', 'vless_vpns')
URL        = f'https://t.me/s/{CHANNEL}'
FETCH_NUM  = 2
OUT_FILE   = 'subscribes.txt'

def fetch_html():
    resp = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
    resp.raise_for_status()
    return resp.text

def extract_bottom_posts(html, n):
    soup   = BeautifulSoup(html, 'html.parser')
    blocks = soup.select('.tgme_widget_message_text')
    # Берём последние n элементов из списка (самые "нижние" на странице)
    bottom = blocks[-n:] if len(blocks) >= n else blocks
    return [blk.get_text(separator='\n', strip=True) for blk in bottom]

def main():
    html  = fetch_html()
    posts = extract_bottom_posts(html, FETCH_NUM)

    if not posts:
        print(f'⚠️ Не найдено ни одного поста в @{CHANNEL}')
        return

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        for post in posts:
            f.write(post + '\n\n')

    print(f'✅ Записано {len(posts)} самых нижних {FETCH_NUM} постов в {OUT_FILE}')

if __name__ == '__main__':
    main()

