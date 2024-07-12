from flask import Flask, render_template, request, redirect
from telebot import TeleBot, types
from database import Database

bot = TeleBot('7058890607:AAGOXcU75-LUn207UjiJvXWpoehcMpEBR-w')

app = Flask(__name__)


def add_user(user_id):
    db = Database('db.db')
    with open('users.txt') as file:
        users = file.read().split()

    users.append(str(user_id))

    db.new_write(table='users', data={'id': user_id})

    del db


def can_send(user_id):
    db = Database('db.db')
    users_id =[user['id'] for user in db.get_data(table='users')]

    del db

    return user_id not in users_id


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

    bot.send_message(-1002165833102, text, parse_mode='Markdown', reply_markup=kb)
    bot.send_message(user_id, '✅ Ваша заявка отправлена на рассмотрение')


@app.route('/<user_id>', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(debug=False)
