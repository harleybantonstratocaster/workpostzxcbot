import datetime
import random
from datetime import datetime
from telethon import TelegramClient, events
from datetime import timedelta
import asyncio

accounts = [
    {"api_id": 28300645, "api_hash": '5f25371da2bf53707fdad2cbf4321d44', "session": 'work1', "name": 'Sophia',
     "listened_phrases": [], "chat_id": -813873054},
    {"api_id": 25842680, "api_hash": 'c9b5f4e951ca79f2c061cf9842c95902', "session": 'work2', "name": 'Natalie',
     "listened_phrases": [], "chat_id": -813873054},
]

phrases = ['1', '2', '3']
banks = ['🟡 Тинькофф', '🟢 СБЕРБАНК', '🅰️ Альфа Банк', '🥝 КИВИ']
operation_types_tinkoff = ['🟡 Баланс (Главная)', '🟡 Баланс (Карта)', '🟡 Получение']
sender_banks = ['🟡 Со сбербанка', '🟡 С тинькофф', '🟡 С киви']
operation_types_sber = ['🟢 Баланс (Главная)', '🟢 Баланс (Карта)']
operation_types_alfa = ['🅰️ Карты (Баланс)', '🅰️ Главная (Баланс)']

listen_time = None
clients = []
queue = []


def format_number(number):
    return "{:,}".format(number).replace(",", " ").replace(".", ",")


async def message_handler(event, client, account):
    global listen_time
    sender = await event.get_sender()
    chat = await event.get_chat()

    if 'start reg' in event.raw_text:
        prev_delay = timedelta(seconds=0)
        for msg, delay in account["listened_phrases"]:
            wait_time = delay - prev_delay
            await asyncio.sleep(wait_time.total_seconds())
            await client.send_message(account["chat_id"], msg)
            prev_delay = delay

    if 'listen' in event.raw_text:
        listen_time = event.date
        for account in accounts:
            account["listened_phrases"].clear()
    print(event.raw_text)
    name = None
    rest_of_message = None
    if ' ' in event.raw_text:
        name, *rest_of_message = event.raw_text.split()
    if name.lower() == account["name"].lower():
        if listen_time:
            message_time = event.date
            difference = message_time - listen_time
            rest_of_message_str = ' '.join(rest_of_message)
            account["listened_phrases"].append((rest_of_message_str, difference))



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
            await client.send_message(account["chat_id"], event.message)

    if 'forget' in event.raw_text:
        for account in accounts:
            account["listened_phrases"].clear()


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
