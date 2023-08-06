import datetime
import random
from datetime import datetime
from telethon import TelegramClient, events
from datetime import timedelta
import asyncio
import json

with open('config.json', 'r') as file:
    config = json.load(file)

accounts = config['accounts']
phrases = config['phrases']
main_api = config['main_api']
banks = ['🟡 Тинькофф', '🟢 СБЕРБАНК', '🅰️ Альфа Банк', '🥝 КИВИ']
operation_types_tinkoff = ['🟡 Баланс (Главная)', '🟡 Баланс (Карта)', '🟡 Получение']
sender_banks = ['🟡 Со сбербанка', '🟡 С тинькофф', '🟡 С киви']
operation_types_sber = ['🟢 Баланс (Главная)', '🟢 Баланс (Карта)']
operation_types_alfa = ['🅰️ Карты (Баланс)', '🅰️ Главная (Баланс)']

listened_phrases = []
listen_time = None
clients = []


def format_number(number):
    return "{:,}".format(number).replace(",", " ").replace(".", ",")


async def message_handler(event, client, account):
    global listen_time, prev_delay
    sender = await event.get_sender()
    if 'start reg' in event.raw_text:
        for msg, name, delay in listened_phrases:
            if name.lower() == account["name"].lower():
                await asyncio.sleep(delay.total_seconds())
                await client.send_message(account["chat_id"], msg)

    if 'listen' in event.raw_text:
        listen_time = event.date
        listened_phrases.clear()
        prev_delay = timedelta(seconds=0)
    if main_api == account["api_id"]:
        if ' ' in event.raw_text:
            name, *rest_of_message = event.raw_text.split()
            if listen_time:
                rest_of_message_str = ' '.join(rest_of_message)
                delay = timedelta(seconds=random.uniform(900, 3600))
                listened_phrases.append((rest_of_message_str, name, delay + prev_delay))
                prev_delay += delay

    if 'start check' in event.raw_text:
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
                        balance = (round(random.uniform(10000, 100000), 2))
                        spendings = (round(random.uniform(10000, 100000), 2))
                        await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                                  format_number(balance) + '\n' +
                                                  format_number(spendings) + '\n' +
                                                  str(random.randint(1111, 9999))
                                                  )
                    case '🟡 Баланс (Главная)':
                        balance = (round(random.uniform(10000, 100000), 2))
                        spendings = (round(random.uniform(10000, 100000), 2))
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
                                summ = (round(random.uniform(10000, 100000), 2))
                                await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                                          format_number(summ) + '\n' +
                                                          datetime.now().strftime("%d %m %y, %H:%M")
                                                          )

                            case _:
                                summ = (round(random.uniform(10000, 100000), 2))
                                await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                                          format_number(summ) + '\n' +
                                                          datetime.now().strftime("%d %m %y, %H:%M") + '\n' +
                                                          account["name"]
                                                          )

            case '🟢 СБЕРБАНК':
                operation_type = random.choice(operation_types_sber)
                await client.send_message('RGT_check4bot', operation_type)
                balance = (round(random.uniform(10000, 100000), 2))
                await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                          format_number(balance) + '\n' +
                                          str(random.randint(1111, 9999))
                                          )
            case '🅰️ Альфа Банк':
                operation_type = random.choice(operation_types_alfa)
                await client.send_message('RGT_check4bot', operation_type)

                match operation_type:

                    case '🅰️ Карты (Баланс)':
                        balance = (round(random.uniform(10000, 100000), 2))
                        await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                                  format_number(balance) + '\n' +
                                                  str(random.randint(1111, 9999)) + '\n' +
                                                  str(random.randint(1111, 9999))
                                                  )

                    case '🅰️ Главная (Баланс)':
                        balance = (round(random.uniform(10000, 100000), 2))
                        await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                                  format_number(balance) + '\n' +
                                                  account["name"] + '\n' +
                                                  str(random.randint(1111, 9999))
                                                  )
            case '🥝 КИВИ':
                await client.send_message('RGT_check4bot', '🥝 Баланс')
                balance = (round(random.uniform(10000, 100000), 2))
                await client.send_message('RGT_check4bot', datetime.now().strftime("%H:%M") + '\n' +
                                          format_number(balance)
                                          )
    if sender.username == 'RGT_check4bot':
        if event.message.photo and not event.message.text:
            await asyncio.sleep(timedelta(seconds=random.uniform(1, 7200)).total_seconds())
            await client.send_message(account["chat_id"],random.choice(phrases),file=event.message)


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
