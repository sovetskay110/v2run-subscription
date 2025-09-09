import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID    = int(os.environ['TELEGRAM_API_ID'])
API_HASH  = os.environ['TELEGRAM_API_HASH']
SESSION   = os.environ['TELEGRAM_SESSION']
CHANNEL   = 'vless_vpns'

async def main():
    # инициализируем клиента из StringSession (а не файла)
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    
    # подключаемся без интерактива
    await client.connect()
    
    # проверяем, что сессия авторизована
    if not await client.is_user_authorized():
        print('❗ Client is not authorized. Проверьте TELEGRAM_SESSION.')
        await client.disconnect()
        return

    # читаем 2 последних сообщения
    msgs = await client.get_messages(CHANNEL, limit=2)
    
    # записываем их в файл (в хронологическом порядке)
    with open('subscribes.txt', 'w', encoding='utf-8') as f:
        for msg in reversed(msgs):
            text = msg.message or ''
            f.write(text.strip() + '\n')

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())


