from flask import Flask, render_template, request, redirect
from telebot import TeleBot, types
from database_server import Database
from config import db_url, bot_token
import utils

bot = TeleBot(bot_token)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


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
    bot.send_message(user_id, '✅ Ваша заявка отправлена на рассмотрение')


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


@app.route('/event/<event_id>')
def events(event_id):

    print('Cookies:', request.cookies)
    print('Headers:', request.headers)
    print('Body:', request.get_data())

    db = Database(db_url)

    event_data = db.get_data(table='events', filters={'id': event_id})[0]

    plan = event_data['plan']
    date = event_data['date']
    event_tech_data = eval(event_data['data'])

    ready = [db.get_data(table='users', filters={'id': user_id})[0]['name'] for user_id in event_tech_data['ready']]
    maybe = [db.get_data(table='users', filters={'id': user_id})[0]['name'] for user_id in event_tech_data['maybe']]
    no = [db.get_data(table='users', filters={'id': user_id})[0]['name'] for user_id in event_tech_data['no']]

    is_expired = utils.is_event_expired(event_id)

    del db
    return render_template('event.html', plan=plan, date=date, ready=ready, maybe=maybe, no=no, event_id=event_id, is_expired=is_expired)


@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run()
