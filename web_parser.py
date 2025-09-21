# web_parser.py

import os
import requests
from bs4 import BeautifulSoup

# Список каналов для парсинга (без @)
# Можно переопределить через ENV: export CHANNELS="vless_vpns,vpn_free_one_day"
CHANNELS      = os.getenv('CHANNELS', 'vless_vpns,vpn_free_one_day').split(',')
URL_TEMPLATE  = 'https://t.me/s/{}'
FETCH_NUM     = 2
OUT_FILE      = 'subscribes.txt'

def fetch_html(channel: str) -> str:
    url = URL_TEMPLATE.format(channel.strip())
    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp.raise_for_status()
    return resp.text

def extract_bottom_posts(html: str, n: int) -> list[str]:
    soup   = BeautifulSoup(html, 'html.parser')
    blocks = soup.select('.tgme_widget_message_text')
    bottom = blocks[-n:] if len(blocks) >= n else blocks
    return [blk.get_text(separator='\n', strip=True) for blk in bottom]

def main():
    merged = []

    for channel in CHANNELS:
        try:
            html  = fetch_html(channel)
        except Exception as e:
            print(f'⚠️ Ошибка при запросе @{channel}: {e}')
            continue

        posts = extract_bottom_posts(html, FETCH_NUM)
        for post in posts:
            lines = post.splitlines()
            for i, line in enumerate(lines):
                text = line.strip()

                # 1) trojan-группа из 3 строк
                if 'trojan' in text.lower():
                    group = lines[i:i+3]
                    merged.append(' '.join(l.strip() for l in group))

                # 2) отдельные vless:// строки
                if 'vless://' in text.lower():
                    merged.append(text)

    # Добавление ключа из секретов Codespaces
    vless1 = os.getenv('VLESS1')
    if vless1:
        merged.append(vless1)

    if not merged:
        print(f'⚠️ Не найдено ни trojan, ни vless в последних {FETCH_NUM} постах каналов {CHANNELS}')
        return

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        for item in merged:
            f.write(item + '\n')

    print(f'✅ Записано {len(merged)} записей (trojan + vless + VLESS1) из каналов {CHANNELS} в {OUT_FILE}')
    print(f'🔍 VLESS1 из ENV: {vless1}')



if __name__ == '__main__':
    main()


