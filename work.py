import datetime
import random
from datetime import datetime
from telethon import TelegramClient, events
from datetime import timedelta
import asyncio
import json

with open('config.json', 'r') as file:
    config = json.load(file)

api_id = config['api_id']
api_hash = config['api_hash']
accounts = config['accounts']
main_session = config['main_session']
main_chat = config['main_chat']
banks = ['🟡 Тинькофф', '🟢 СБЕРБАНК', '🅰️ Альфа Банк', '🥝 КИВИ']
operation_types_tinkoff = ['🟡 Баланс (Главная)', '🟡 Баланс (Карта)', '🟡 Получение']
sender_banks = ['🟡 Со сбербанка', '🟡 С тинькофф', '🟡 С киви']
operation_types_sber = ['🟢 Баланс (Главная)', '🟢 Баланс (Карта)']
operation_types_alfa = ['🅰️ Карты (Баланс)', '🅰️ Главная (Баланс)']

listened_phrases = []
listen_time = None
clients = []
pending_messages = {}


def format_number(number):
    return "{:,}".format(number).replace(",", " ").replace(".", ",")


async def message_handler(event, client, account):
    global listen_time, prev_delay
    sender = await event.get_sender()

    if 'start reg' in event.raw_text:
        for msg, name, delay, needs_check, bal_range in listened_phrases:
            await asyncio.sleep(delay.total_seconds())
            if name.lower() == account["name"].lower():
                if needs_check:
                    await generate_check(client, name, msg,bal_range)
                else:
                    await client.send_message(account["chat_id_1"], msg)
                    await client.send_message(account["chat_id_2"], msg)

    if sender.username == 'RGT_check4bot':
        if event.message.photo and not event.message.text:
            intended_msg = pending_messages.get(account["name"].lower(), None)
            if intended_msg:
                await client.send_message(account["chat_id_1"], intended_msg, file=event.message.media)
                await client.send_message(account["chat_id_2"], intended_msg, file=event.message.media)
                del pending_messages[account["name"].lower()]

    if 'listen' in event.raw_text:
        listen_time = event.date
        listened_phrases.clear()
    if main_session == account["session"] and event.chat_id == main_chat:
        if ' ' in event.raw_text:
            bal = None
            needs_check = False
            name, *rest_of_message = event.raw_text.split()
            if listen_time:
                rest_of_message_str = ' '.join(rest_of_message)
                if '(чек)' in rest_of_message_str:
                    rest_of_message_str = rest_of_message_str.replace('(чек)', '')
                    needs_check = True
                    bal = '<70'
                if '(чек>70)' in rest_of_message_str:
                    rest_of_message_str = rest_of_message_str.replace('(чек>70) ', '')
                    needs_check = True
                    bal = '>70'
                delay = timedelta(seconds=random.uniform(10, 60))
                listened_phrases.append((rest_of_message_str, name, delay, needs_check,bal))
                print(listened_phrases)


async def generate_check(client, name, msg,bal_range):
    if bal_range == '<70':
        r1 = 10000
        r2 = 100000
    else:
        r1 = 100000
        r2 = 200000
    has_dialog = False
    async for message in client.iter_messages('RGT_check4bot'):
        has_dialog = True
        break
    if not has_dialog:
        await client.send_message('RGT_check4bot', '/start')

    await client.send_message('RGT_check4bot', 'Чеки / Балансы')

    bank = random.choice(banks)
    await client.send_message('RGT_check4bot', bank)

    match bank:

        case '🟡 Тинькофф':
            operation_type = random.choice(operation_types_tinkoff)
            await client.send_message('RGT_check4bot', operation_type)

            match operation_type:

                case '🟡 Баланс (Карта)':
                    balance = (round(random.uniform(r1, r2), 2))
                    spendings = (round(random.uniform(r1, r2), 2))
                    await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                              format_number(balance) + '\n' +
                                              format_number(spendings) + '\n' +
                                              str(random.randint(1111, 9999))
                                              )
                case '🟡 Баланс (Главная)':
                    balance = (round(random.uniform(r1, r2), 2))
                    spendings = (round(random.uniform(r1, r2), 2))
                    await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                              account["name"] + '\n' +
                                              format_number(balance) + '\n' +
                                              format_number(spendings) + '\n' +
                                              str(random.randint(1111, 9999))
                                              )

                case '🟡 Получение':
                    sender_bank = random.choice(sender_banks)
                    await client.send_message('RGT_check4bot', sender_bank)

                    match sender_bank:

                        case '🟡 С киви':
                            summ = (round(random.uniform(r1, r2), 2))
                            await client.send_message('RGT_check4bot',
                                                      datetime.now().strftime("%H:%M") + '\n' +
                                                      format_number(summ) + '\n' +
                                                      datetime.now().strftime("%d %m %y, %H:%M")
                                                      )

                        case _:
                            summ = (round(random.uniform(r1, r2), 2))
                            await client.send_message('RGT_check4bot',
                                                      datetime.now().strftime("%H:%M") + '\n' +
                                                      format_number(summ) + '\n' +
                                                      datetime.now().strftime(
                                                          "%d %m %y, %H:%M") + '\n' +
                                                      'Сергей'
                                                      )

        case '🟢 СБЕРБАНК':
            operation_type = random.choice(operation_types_sber)
            await client.send_message('RGT_check4bot', operation_type)
            balance = (round(random.uniform(r1, r2), 2))
            await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                      format_number(balance) + '\n' +
                                      str(random.randint(1111, 9999))
                                      )
        case '🅰️ Альфа Банк':
            operation_type = random.choice(operation_types_alfa)
            await client.send_message('RGT_check4bot', operation_type)

            match operation_type:

                case '🅰️ Карты (Баланс)':
                    balance = (round(random.uniform(r1, r2), 2))
                    await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                              format_number(balance) + '\n' +
                                              str(random.randint(1111, 9999)) + '\n' +
                                              str(random.randint(1111, 9999))
                                              )

                case '🅰️ Главная (Баланс)':
                    balance = (round(random.uniform(r1, r2), 2))
                    await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                              format_number(balance) + '\n' +
                                              account["name"] + '\n' +
                                              str(random.randint(1111, 9999))
                                              )
        case '🥝 КИВИ':
            await client.send_message('RGT_check4bot', '🥝 Баланс')
            balance = (round(random.uniform(r1, r2), 2))
            await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                      format_number(balance)
                                      )
    pending_messages[name] = msg


def bind_event_handler(client, account):
    client.on(events.NewMessage())(lambda event: message_handler(event, client, account))


for account in accounts:
    client = TelegramClient(account['session'], api_id, api_hash)
    bind_event_handler(client, account)
    clients.append(client)

for client in clients:
    client.start()

for client in clients:
    client.run_until_disconnected()
