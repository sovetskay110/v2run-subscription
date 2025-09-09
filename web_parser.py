# web_parser.py

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
    bottom = blocks[-n:] if len(blocks) >= n else blocks
    return [blk.get_text(separator='\n', strip=True) for blk in bottom]

def main():
    html  = fetch_html()
    posts = extract_bottom_posts(html, FETCH_NUM)

    merged = []
    for post in posts:
        lines = post.splitlines()
        for i, line in enumerate(lines):
            if 'trojan' in line.lower():
                group = lines[i:i+3]
                merged.append(' '.join(l.strip() for l in group))

    if not merged:
        print(f'⚠️ Не найдено строк с trojan в последних {FETCH_NUM} постах')
        return

    # текущая дата в формате DD_MM
    date_str = datetime.now().strftime('%d_%m')

    # заменяем в каждой склеенной строке суффикс 'vpns' на дату
    processed = []
    for item in merged:
        if item.endswith('vpns'):
            item = item[:-4] + date_str
        processed.append(item)

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        for line in processed:
            f.write(line + '\n')

    print(f'✅ Записано {len(processed)} склеенных строк в {OUT_FILE}')

if __name__ == '__main__':
    main()
