from loader import app
from flask import Flask, render_template, request, redirect, make_response
from database_server import Database
from config import db_url
import utils
import requests

from datetime import datetime


@app.route('/api/get_profile_data')
def get_profile_data():
    db = Database(db_url)

    user = db.get_data(table='users', filters={'id': request.args.get('user_id')})[0]

    if user['birthday']:
        birthday = datetime.strptime(user['birthday'], '%d.%m.%Y')
        now = datetime.now()
        age = now.year - birthday.year - ((now.month, now.day) < (birthday.month, birthday.day))
        user['age'] = age
        user['zodiac'] = utils.get_zodiac_sign(birthday)
        user['birthday'] = birthday.strftime('%d.%m.%Y')

    create_timestamp = str(user['create_timestamp'])
    create_date = datetime.fromtimestamp(int(create_timestamp)).strftime('%d.%m.%Y')
    days_from_create = (datetime.now() - datetime.fromtimestamp(int(create_timestamp))).days
    user['create_date'] = create_date
    user['days_from_create'] = days_from_create

    user['stats'] = utils.get_stats(user_id=user['id'])

    return user


@app.route('/api/edit_about', methods=['POST'])
def edit_about():
    data = request.get_json()

    user_id = data['user_id']
    about = data['about']

    db = Database(db_url)

    db.update_data(data={'about': about}, filters={'id': user_id}, table='users')

    return {'status': 'ok'}


@app.route('/api/edit_birthday', methods=['POST'])
def edit_birthday():
    data = request.get_json()

    user_id = data['user_id']
    birthday = data['birthday']

    db = Database(db_url)

    if not birthday:
        db.update_data(data={'birthday': None}, filters={'id': user_id}, table='users')
        return {'birthday': None, 'status': 'ok'}
    
    birthday = datetime.strptime(birthday, '%Y-%m-%d')


    db.update_data(data={'birthday': birthday.strftime('%d.%m.%Y')}, filters={'id': user_id}, table='users')

    now = datetime.now()
    age = now.year - birthday.year - ((now.month, now.day) < (birthday.month, birthday.day))

    return {'status': 'ok', 'age': age, 'zodiac': utils.get_zodiac_sign(birthday), 'birthday': birthday.strftime('%d.%m.%Y')}


@app.route('/api/analyze_user', methods=['POST'])
def analyze_user():
    data = request.get_json()
    user_id = data['user_id']

    db = Database(db_url)

    messages = db.get_data(table='analyze', filters={'owner': user_id})[-50:]
    user = db.get_data(table='users', filters={'id': user_id})[0]

    curent_culture_index = user['culture_index']
    curent_friendly_index = user['friendly_index']
    curent_respons_index = user['respons_index']

    if messages:
        text = '\n\n'.join([message['text'] for message in messages])
        result = utils.analyze_text(text)

        new_culture_index = result['culture_index']
        new_friendly_index = result['friendly_index']
        new_respons_index = result['respons_index']

        db.update_data(data={'culture_index': new_culture_index, 'friendly_index': new_friendly_index, 'respons_index': new_respons_index}, filters={'id': user_id}, table='users')

    else:
        new_culture_index = curent_culture_index
        new_friendly_index = curent_friendly_index
        new_respons_index = curent_respons_index

    return {'culture_index': new_culture_index, 'friendly_index': new_friendly_index, 'respons_index': new_respons_index}


@app.route('/api/analyze_user_text', methods=['POST'])
def analyze_user_text():
    data = request.get_json()
    user_id = data['user_id']

    db = Database(db_url)

    messages = db.get_data(table='analyze', filters={'owner': user_id})[-50:]

    if not messages:
        return 'Не удалось проанализировать 😢'

    text = '\n\n'.join([message['text'] for message in messages])
    result = utils.analyze_text(text, mode='comment')    

    response = make_response({'result': result})
    response.headers['Cache-Control'] = 'public, max-age=120'

    return response