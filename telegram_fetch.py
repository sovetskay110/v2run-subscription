import os, asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID   = int(os.environ['TELEGRAM_API_ID'])
API_HASH = os.environ['TELEGRAM_API_HASH']
SESSION  = os.environ['TELEGRAM_SESSION']
CHANNEL  = 'vless_vpns'

async def main():
    # Подключаемся к уже существующему сеансу
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print('❗ Session невалидна — проверьте секрет TELEGRAM_SESSION')
        return

    # Читаем два последних сообщения и записываем в файл
    msgs = await client.get_messages(CHANNEL, limit=2)
    with open('subscribes.txt', 'w', encoding='utf-8') as f:
        for m in reversed(msgs):
            f.write((m.message or '').strip() + '\n')

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())


