from telethon import TelegramClient, events
from datetime import timedelta
import asyncio

accounts = [
    {"api_id": 28300645, "api_hash": '5f25371da2bf53707fdad2cbf4321d44', "session": 'work1', "name": 'Sophia',"listened_phrases": []},
    {"api_id": 25842680, "api_hash": 'c9b5f4e951ca79f2c061cf9842c95902', "session": 'work2', "name": 'Natalie',"listened_phrases": []},
]

phrases = ['1', '2', '3']

listen_time = None
clients = []


async def message_handler(event, client, account):
    global listen_time
    sender = await event.get_sender()

    if 'start_reg' in event.raw_text:
        prev_delay = timedelta(seconds=0)
        for msg, delay in account["listened_phrases"]:
            wait_time = delay - prev_delay
            await asyncio.sleep(wait_time.total_seconds())
            await client.send_message(event.chat_id, msg)
            prev_delay = delay

    if 'start check' in event.raw_text:
        has_dialog = False
        async for message in client.iter_messages('RGT_check4bot'):
            has_dialog = True
            break
        if not has_dialog:
            await client.send_message('RGT_check4bot', '/start')

    if 'forget' in event.raw_text:
        for account in accounts:
            account["listened_phrases"].clear()

    if 'listen' in event.raw_text:
        listen_time = event.date
        for account in accounts:
            account["listened_phrases"].clear()
    if sender.first_name == account["name"]:
        if listen_time:
            message_time = event.date
            difference = message_time - listen_time
            account["listened_phrases"].append((event.raw_text, difference))


def bind_event_handler(client, account):
    client.on(events.NewMessage())(lambda event: message_handler(event, client, account))


for account in accounts:
    client = TelegramClient(account['session'], account['api_id'], account['api_hash'])
    bind_event_handler(client, account)
    clients.append(client)

for client in clients:
    client.start()

for client in clients:
    client.run_until_disconnected()
