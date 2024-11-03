import datetime
from database_server import Database
from config import db_url, GROUP_ID_ALCO, GROUP_ID_CHLB, GROUP_ID, ADMIN_ID_ADD, GROUP_ID_ADD
from datetime import datetime, timedelta, timezone

from config import bot_token, promt, promt_neuro_comment
from telebot import TeleBot, types
import emoji
from loader import bot, db, chatgpt

from g4f.models import gpt_4o_mini

import requests


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
    if user_id == ADMIN_ID_ADD:
        return 'add_admin'

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


def split_by_emoji(text):
    res = []
    temp = ''
    for char in text:
        if emoji.is_emoji(char):
            if temp:
                temp = temp.strip()
                temp = temp.replace('\n', '')
                temp = temp.replace('*', '')                
                res.append(temp)
                temp = ''
        temp += char

    if temp:
        temp = temp.strip()
        temp = temp.replace('\n', '')
        temp = temp.replace('*', '')
        res.append(temp)
    return res



def add_user(user_id):
    db = Database(db_url)

    db.update_data(data={'is_form': True}, filters={'id': user_id}, table='users')

    del db

def can_send(user_id):
    db = Database(db_url)
    user_data = db.get_data(table='users', filters={'id': user_id})[0]

    del db

    return not bool(user_data['is_form'])


def escape_markdown(text):
    special_chars = ['_', '*', '[', ']', '(', ')']

    for char in special_chars:
        text = text.replace(char, '\\' + char)

    return text

def make_beautiful_text(from_data):
    finds_tags = ['friends', 'drinkingBuddies', 'oneNight', 'romantic', 'likeMinded', 'alone']
    interests_tags = ['music', 'walking', 'walkingWithAlcohol', 'art', 'cozyPlaces', 'injections', 'boardGames', 'hookah', 'gaming', 'bar', 'sports', 'club', 'hiking'
                      'tea', 'coffee', 'longTrips']

    name = escape_markdown(from_data['name'])
    age = escape_markdown(str(from_data['age']))
    city = escape_markdown(from_data['city'])
    from_where = escape_markdown(from_data['fromWhere'])
    about = escape_markdown(from_data['about'])
    drinking = escape_markdown(from_data['drinkingFrequency'])
    finds = ', '.join([escape_markdown(from_data[tag]) for tag in from_data if tag in finds_tags])
    interests = ', '.join([escape_markdown(from_data[tag]) for tag in from_data if tag in interests_tags])
    bad_things = escape_markdown(from_data['badThings'])
    social_media = escape_markdown(from_data['socialMedia'])
    conflict_level = escape_markdown(from_data['conflictLevel'])
    new_people = escape_markdown(from_data['newPeopleAttitude'])
    link = escape_markdown(from_data['link'])
    
    text = ('*Информация о пользователе:*\n\n'
            f'*Имя:* {name}\n'
            f'*Возраст:* {age} лет\n'
            f'*Город проживания:* {city}\n'
            f'*Откуда:* {from_where}\n'
            f'*О себе:* {about}\n'
            f'*Отношение к алкоголю:* {drinking}\n'
            f'*Хочу найти:* {finds}\n'
            f'*Интересы:* {interests}\n'
            f'*Плохие привычки:* {bad_things}\n'
            f'*Социальные сети:* {social_media}\n'
            f'*Уровень конфликтности:* {conflict_level}\n'
            f'*Отношение к новичкам:* {new_people}\n'
            f'*Ссылка на профиль:* {link}\n')

    return text


def send_message(user_id, text):
    btn_1 = types.InlineKeyboardButton(text='✅', callback_data=f'invite:pre_accept:{user_id}')
    btn_2 = types.InlineKeyboardButton(text='❌', callback_data=f'invite:pre_decline:{user_id}')

    kb = types.InlineKeyboardMarkup().row(btn_1, btn_2)

    bot.send_message(-1002165833102, text, parse_mode='Markdown', reply_markup=kb) # -1002165833102

    btn_1 = types.InlineKeyboardButton(text='Подписаться', url='https://t.me/novotropsk_global')
    kb = types.InlineKeyboardMarkup().row(btn_1)
    bot.send_message(user_id, '✅ *Ваша заявка отправлена на рассмотрение.* Пока ждете, можете подписаться на наш канал! \n\nhttps://t.me/novotropsk\_global', parse_mode='Markdown', reply_markup=kb)    



def beautify_date(date_str):
    """
    Beautify date string.
    If date is today, tomorrow or the day after tomorrow, return string representation of this day.
    Otherwise, return original string.
    """
    from datetime import datetime, timedelta

    date = datetime.strptime(date_str, '%d.%m.%Y')
    today = datetime.today()
    delta = date - today

    print(delta.days)

    if delta.days == -1:
        return 'Сегодня'
    elif delta.days == 0:
        return 'Завтра'
    elif delta.days == 1:
        return 'Послезавтра'
    else:
        return date_str
    

def get_file_url(file_id):
    # Шаг 1: Получить путь к файлу с помощью file_id
    url_get_file = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
    response = requests.get(url_get_file)
    response_data = response.json()
    
    if not response_data['ok']:
        raise Exception(f"Ошибка при получении информации о файле: {response_data['description']}")
    
    # Извлекаем file_path из ответа
    file_path = response_data['result']['file_path']
    
    # Шаг 2: Сформировать ссылку для скачивания файла
    download_link = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
    return download_link


def analyze_text(text, mode='parameters'):
    if mode == 'parameters':
        response = chatgpt.chat.completions.create(
            # model='gpt-3.5-turbo',
            model=gpt_4o_mini,
            provider='Pizzagpt',
            messages=[
                {"role": "user", "content": promt},
                {"role": "user", "content": f'{text}'}
            ]
        )
        print(response.choices[0].message.content)
        data = response.choices[0].message.content.split(', ')
        print()
        print(data)

        # return

        culture_index = int(data[0].split()[-1])
        friendly_index = int(data[1].split()[-1])
        respons_index = int(data[2].split()[-1])

        return {
            'culture_index': culture_index,
            'friendly_index': friendly_index,
            'respons_index': respons_index
        }
    
    elif mode == 'comment':
        neuro_comment = chatgpt.chat.completions.create(
            model=gpt_4o_mini,
            provider='Pizzagpt',
            messages=[
                {"role": "user", "content": f'{promt_neuro_comment} \n\n{text}'}
            ]
        )
        print(neuro_comment.choices[0].message.content)

        neuro_comment = neuro_comment.choices[0].message.content

        return neuro_comment        


def get_bot_username():
    bot_data = bot.get_me()

    return bot_data.username


def get_zodiac_sign(birthday):
        if (birthday.month == 3 and birthday.day >= 21) or (birthday.month == 4 and birthday.day <= 19):
            return 'Овен'
        if (birthday.month == 3 and birthday.day >= 21) or (birthday.month == 4 and birthday.day <= 19):
            return 'Овен'
        elif (birthday.month == 4 and birthday.day >= 20) or (birthday.month == 5 and birthday.day <= 20):
            return 'Телец'
        elif (birthday.month == 5 and birthday.day >= 21) or (birthday.month == 6 and birthday.day <= 20):
            return 'Близнецы'
        elif (birthday.month == 6 and birthday.day >= 21) or (birthday.month == 7 and birthday.day <= 22):
            return 'Рак'
        elif (birthday.month == 7 and birthday.day >= 23) or (birthday.month == 8 and birthday.day <= 22):
            return 'Лев'
        elif (birthday.month == 8 and birthday.day >= 23) or (birthday.month == 9 and birthday.day <= 22):
            return 'Дева'
        elif (birthday.month == 9 and birthday.day >= 23) or (birthday.month == 10 and birthday.day <= 22):
            return 'Весы'
        elif (birthday.month == 10 and birthday.day >= 23) or (birthday.month == 11 and birthday.day <= 21):
            return 'Скорпион'
        elif (birthday.month == 11 and birthday.day >= 22) or (birthday.month == 12 and birthday.day <= 21):
            return 'Стрелец'
        elif (birthday.month == 12 and birthday.day >= 22) or (birthday.month == 1 and birthday.day <= 19):
            return 'Козерог'
        elif (birthday.month == 1 and birthday.day >= 20) or (birthday.month == 2 and birthday.day <= 18):
            return 'Водолей'
        elif (birthday.month == 2 and birthday.day >= 19) or (birthday.month == 3 and birthday.day <= 20):
            return 'Рыбы'


def get_stats(user_id):
    total_msg = len(db.get_data(table='analyze', filters={'owner': user_id}))

    # ----

    total_votes = 0

    for event in db.get_data(table='events', filters={'type': 'event'}):
        event_data = eval(event['data'])

        if user_id in event_data['ready'] + event_data['maybe'] + event_data['no']:
            total_votes += 1

    total_events = len(db.get_data(table='events', filters={'type': 'event'}))

    skip_procent = (total_events - total_votes) / total_events * 100

    return {
        'total_msg': total_msg,
        'total_votes': total_votes,
        'skip_procent': skip_procent
    }


def analyze_user(user_id):
    messages = db.get_data(table='analyze', filters={'owner': user_id})[-1000:]

    print(messages)

    if not messages:
        return 'Не удалось проанализировать 😢'

    text = '\n\n'.join([message['text'] for message in messages])
    result = analyze_text(text, mode='comment')

    return result


# analyze_user(5061120370)