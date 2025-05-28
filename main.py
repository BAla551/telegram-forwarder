import asyncio
import time
from telethon import TelegramClient, events

# --- TELETHON CONFIG ---
api_id = 25440549
api_hash = 'c13c2b66dccce92a8c95e4de3adbf533'
session_name = 'link_forwarder'

source_channels = ['@telugutechtuts', '@TechFactsDeals']
target_bot = '@ExtraPeBot'

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        print(f'[✓] New message received: {event.id}')
        await client.forward_messages(target_bot, event.message)
        print(f'[✓] Message {event.id} forwarded to {target_bot}')
    except Exception as e:
        print(f'[!] Error forwarding message {event.id}: {e}')

async def run_client():
    print('[✓] Starting Telegram client...')
    await client.start()
    print('[✓] Listening 24/7 for new messages...')
    await client.run_until_disconnected()

async def main():
    while True:
        try:
            await run_client()
        except Exception as e:
            print(f'[!] Client crashed with error: {e}')
            print('[!] Restarting in 10 seconds...')
            await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())
