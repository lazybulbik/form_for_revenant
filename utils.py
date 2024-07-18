import datetime
from database_server import Database
from config import db_url, GROUP_ID_ALCO, GROUP_ID_CHLB, GROUP_ID
from datetime import datetime, timedelta, timezone

from config import bot_token
from telebot import TeleBot, types



db = Database(db_url)
bot = TeleBot(bot_token)

def get_current_time_ekaterinburg():
    # Временная зона Екатеринбурга (UTC+5)
    return datetime.utcnow() + timedelta(hours=5)


def time_difference_in_hours(input_time_str):
    ekaterinburg_now = get_current_time_ekaterinburg()
    
    # Парсинг строки времени
    input_time = datetime.strptime(input_time_str, "%d.%m.%Y %H:%M")
    
    # Вычисление разности во времени в часах
    time_difference = input_time - ekaterinburg_now
    time_difference_in_hours = time_difference.total_seconds() / 3600
    
    return time_difference_in_hours


def is_event_expired(event_id):
    event = db.get_data(table='events', filters={'id': event_id})[0]
    event_time = f"{event['date']} {event['time']}"

    if time_difference_in_hours(event_time) <= 0:
        return True

    return False


def is_admin(user_id):
    print('Checking admin', user_id)
    try:
        user = bot.get_chat_member(-1002165833102, user_id)
        print(user)
        if user.status == 'left' or user.status == 'kicked':
            return False
        return True
    except Exception as e:
        print(e)
        return False    


def is_sub(user_id):
    try:
        user = bot.get_chat_member(-1002152346226, user_id)
        # print(user)
        if user.status == 'left' or user.status == 'kicked':
            return False
        return True
    except Exception as e:
        print(e)
        return False        


def get_event_menu(event_id):
    event = db.get_data(table='events', filters={'id': event_id})[0]

    photo = event['photo']
    text = event['text']

    event_data = eval(db.get_data(table='events', filters={'id': event_id})[0]['data'])

    blacklist = list(map(str, event_data['blacklist']))

    go_len = len([user for user in event_data['ready'] if str(user) not in blacklist])
    maybe_len = len([user for user in event_data['maybe'] if str(user) not in blacklist])
    no_len = len(event_data['no'])

    status_event_type = 'Частное' if event_data['blacklist'] else 'Открытое'
    text += f'\n🔐 *Тип мероприятия:* {status_event_type}'

    btn_1 = types.InlineKeyboardButton(text=f'✅ Иду ({go_len})', callback_data=f'event:choose:ready:{event_id}')
    btn_2 = types.InlineKeyboardButton(text=f'☑️ Может быть приду ({maybe_len})',
                                        callback_data=f'event:choose:maybe:{event_id}')
    btn_3 = types.InlineKeyboardButton(text=f'⛔️ Не приду ({no_len})', callback_data=f'event:choose:no:{event_id}')
    btn_4 = types.InlineKeyboardButton(text='⚙️ Подробнее', url=f'https://t.me/Novotropsk_bot/EventSettings?startapp={event_id}')

    kb = types.InlineKeyboardMarkup().row(btn_1, btn_2).row(btn_3).row(btn_4)

    return photo, text, kb        



def get_chanel_id(name):
    return {'ekb': GROUP_ID, 'alco': GROUP_ID_ALCO, 'chlb': GROUP_ID_CHLB}[name]