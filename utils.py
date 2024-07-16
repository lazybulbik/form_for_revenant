import datetime
from database_server import Database
from config import db_url
from datetime import datetime, timedelta, timezone

from config import bot_token
from telebot import TeleBot

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
