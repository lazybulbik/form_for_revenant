from flask import Flask, render_template, request, redirect
from telebot import TeleBot, types
from database_server import Database
from config import db_url, bot_token
import utils

import time

from threading import Thread

bot = TeleBot(bot_token)

app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True

# @app.after_request
# def disable_caching(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Pragma"] = "no-cache"
#     response.headers["Expires"] = "0"
#     return response

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


@app.route('/form/<user_id>', methods=['GET', 'POST'])
def index(user_id):
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        send_message(user_id, make_beautiful_text(form_data))
        add_user(user_id)
        # print(form_data)

        return redirect('/finish')
    else:
        if can_send(user_id):
            return render_template('form.html')
        else:
            return redirect('/nope')
    

@app.route('/finish')
def finish():
    return render_template('finish.html')


@app.route('/nope')
def nope():
    return render_template('nope.html')


@app.route('/event')
def events_list():
    args = request.args
    if args:
        event_id = args.get('tgWebAppStartParam')

        return redirect('/event/' + event_id)


@app.route('/event/<event_id>')
def events(event_id):
    anticash = time.time()
    db = Database(db_url)

    event_data = db.get_data(table='events', filters={'id': event_id})[0]

    plan = event_data['plan']
    date = event_data['date']
    event_tech_data = eval(event_data['data'])

    ready = [db.get_data(table='users', filters={'id': user_id})[0]['name'] for user_id in event_tech_data['ready']]
    maybe = [db.get_data(table='users', filters={'id': user_id})[0]['name'] for user_id in event_tech_data['maybe']]
    no = [db.get_data(table='users', filters={'id': user_id})[0]['name'] for user_id in event_tech_data['no']]

    ready = ready + maybe

    is_expired = utils.is_event_expired(event_id)

    del db
    return render_template('event.html', plan=plan, date=date, ready=ready, maybe=maybe, no=no, event_id=event_id, is_expired=is_expired, anticash=anticash)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/api/is_admin', methods=['POST'])
def is_admin():
    data = request.get_json()

    user_id = data['user_id']
    event_id = data['event_id']

    print(user_id, event_id)

    db = Database(db_url)

    is_admin = utils.is_admin(user_id)

    event_data = db.get_data(table='events', filters={'id': event_id})[0]

    del db

    if is_admin == 'add_admin' and event_data['city'] == 'add':
        return {'status': True}
    
    return {'status': is_admin or event_data['creator'] == user_id}


@app.route('/api/users_notify', methods=['POST'])
def users_notify():
    data = request.get_json()

    user_id = data['user_id']
    event_id = data['event_id']

    db = Database(db_url)

    event_data = eval(db.get_data(table='events', filters={'id': event_id})[0]['data'])
    notify = event_data['notify']

    result = {
        '2': user_id in notify['2'],
        '4': user_id in notify['4'],
        '24': user_id in notify['24'],
        '72': user_id in notify['72'],
        '168': user_id in notify['168'],
    }

    del db

    return result


@app.route('/api/set_notify', methods=['POST'])
def set_notify():
    data = request.get_json()

    user_id = data['user_id']
    event_id = data['event_id']
    notify_id = data['notify']

    db = Database(db_url)

    event_data = eval(db.get_data(table='events', filters={'id': event_id})[0]['data'])


    if user_id in event_data['notify'][notify_id]:
        event_data['notify'][notify_id].remove(user_id)
        db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')
        del db
        return {'status': 'remove'}
    else:
        event_data['notify'][notify_id].append(user_id)
        db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')
        del db
        return {'status': 'add'}


@app.route('/api/users_list', methods=['POST'])
def users_list():
    data = request.get_json()

    event_id = data['event_id']

    db = Database(db_url)

    event_data = eval(db.get_data(table='events', filters={'id': event_id})[0]['data'])

    result = []

    for user in event_data['ready'] + event_data['maybe']:
        user_data = db.get_data(table='users', filters={'id': user})[0]

        result.append({
            'name': user_data['name'],
            'kick': user in event_data['blacklist'],
            'id': user
        })

    del db

    return result


@app.route('/api/kick_user', methods=['POST'])
def kick_user():
    data = request.get_json()

    user_id = data['user_id']
    event_id = data['event_id']

    db = Database(db_url)

    event = db.get_data(table='events', filters={'id': event_id})[0]
    event_data = eval(event['data'])

    chat_id = utils.get_chanel_id(event['city'])

    user_name = db.get_data(table='users', filters={'id': user_id})[0]['name']
    if user_id in event_data['blacklist']:
        event_data['blacklist'].remove(user_id)
        db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')

        del db

        photo, text, kb = utils.get_event_menu(event_id)
        try:
            bot.edit_message_text(chat_id=chat_id, text=text, message_id=event_data['message_id'], reply_markup=kb, parse_mode='Markdown')        
        except Exception as e:
            print(e)
            try:
                bot.edit_message_caption(chat_id=chat_id, caption=text, message_id=event_data['message_id'], reply_markup=kb, parse_mode='Markdown')
            except Exception as e:
                print(e)
                pass

        return {'status': 'remove', 'name': user_name}
    else:
        event_data['blacklist'].append(user_id)
        db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')

        del db

        photo, text, kb = utils.get_event_menu(event_id)
        try:
            bot.edit_message_text(chat_id=chat_id, text=text, message_id=event_data['message_id'], reply_markup=kb, parse_mode='Markdown')        
        except Exception as e:
            print(e)
            try:
                bot.edit_message_caption(chat_id=chat_id, caption=text, message_id=event_data['message_id'], reply_markup=kb, parse_mode='Markdown')
            except Exception as e:
                print(e)
                pass

        return {'status': 'kick', 'name': user_name}

@app.route('/event/<event_id>/cancel', methods=['POST', 'GET'])
def cancel(event_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        db = Database(db_url)

        print(data)

        event = db.get_data(table='events', filters={'id': event_id})[0]
        event_data = eval(event['data'])

        chat_id = utils.get_chanel_id(event['city'])

        tech_msg = event_data['message_id']

        btn = types.InlineKeyboardButton(text='⚠️ Мероприятие отменено', callback_data='None')
        kb = types.InlineKeyboardMarkup().row(btn)

        cancel_text = f'К сожалению, мероприятие отменено. \n\nПричина: {data["reason"]}'

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=tech_msg, reply_markup=kb)

        for user in event_data['ready'] + event_data['maybe']:
            photo = types.InputFile('static/1.jpg')
            bot.send_photo(user, photo=photo, caption=cancel_text)

            time.sleep(1.5)

        del db

        return render_template('ok.html', message='Мероприятие отменено')
    else:
        return render_template('cancel.html', event_id=event_id, anticash=time.time())



def make_mainiling(event_id, data):
    db = Database(db_url)

    print(data)

    event_data = eval(db.get_data(table='events', filters={'id': event_id})[0]['data'])

    for user in event_data['ready'] + event_data['maybe']:
        try:
            if str(user) in list(map(str, event_data['blacklist'])):
                continue

            bot.send_message(user, data['message'])

            time.sleep(0.5)
        except:
            pass

    del db


@app.route('/event/<event_id>/mailing', methods=['POST', 'GET'])
def mailing(event_id):
    if request.method == 'POST':
        data = request.form.to_dict()

        Thread(target=make_mainiling, args=(event_id, data)).start()

        return render_template('ok.html', message='Рассылка запущена')

    else:
        return render_template('mailing.html', event_id=event_id, anticash=time.time())


@app.route('/event/<event_id>/complete', methods=['POST', 'GET'])
def complete(event_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        db = Database(db_url)

        print(data)

        event = db.get_data(table='events', filters={'id': event_id})[0]
        event_data = eval(event['data'])
        tech_msg = event_data['message_id']
        chat_id = utils.get_chanel_id(event['city'])

        btn = types.InlineKeyboardButton(text='✅ Мероприятие завершено', callback_data='None')
        kb = types.InlineKeyboardMarkup().row(btn)

        if data['link']:
            btn_1 = types.InlineKeyboardButton(text='📷 Фотографии', url=data['link'])
            btn_2 = types.InlineKeyboardButton(text='👀 Подписаться на канал с фото', url='https://t.me/+DuBqBtAQVj00YmMy')

            kb.row(btn_1).row(btn_2)

        bot.edit_message_reply_markup(chat_id=chat_id, message_id=tech_msg, reply_markup=kb)

        return render_template('ok.html', message='Мероприятие завершено')

    else:
        return render_template('complete.html', event_id=event_id, anticash=time.time())

@app.route('/event/<event_id>/remind')
def remind(event_id,):
    return render_template('remind.html', event_id=event_id, anticash=time.time())


@app.route('/event/<event_id>/kick')
def kick(event_id,):
    return render_template('kick.html', event_id=event_id, anticash=time.time())


if __name__ == '__main__':
    app.run(debug=True, port=5050)
