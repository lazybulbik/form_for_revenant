from loader import app
from flask import Flask, render_template, request, redirect
from database_server import Database
from config import db_url
import utils
import requests

from datetime import datetime


@app.route('/api/get_event_data', methods=['POST'])
def get_event_data():
    data = request.get_json()

    event_id = data['event_id']
    user_id = data['user_id']

    db = Database(db_url)
    event = db.get_data(table='events', filters={'id': event_id})[0]
    event_data = eval(event['data'])

    user_vote = None
    if str(user_id) in str(event_data['ready']):
        user_vote = 'ready'
    elif str(user_id) in str(event_data['maybe']):
        user_vote = 'maybe'
    elif str(user_id) in str(event_data['no']):
        user_vote = 'no'    

    plan = event['plan']
    date = event['date']
    time = event['time']
    adress = event['address']
    note = event['note']
    event_type = "Частное" if len(event_data['blacklist']) != 0 else "Открытое"
    creator = event['creator_username']
    event_status = event_data['status']
    is_expired = utils.is_event_expired(event_id)
    emoji = event['text'][0]

    ready_users = [{'name': db.get_data(table='users', filters={'id': user})[0]['name'], 'id': user} for user in event_data['ready']]
    maybe_users = [{'name': db.get_data(table='users', filters={'id': user})[0]['name'], 'id': user} for user in event_data['maybe']]
    no_users = [{'name': db.get_data(table='users', filters={'id': user})[0]['name'], 'id': user} for user in event_data['no']]
    map_link = f'https://yandex.ru/maps/?text={"+".join(adress.split())}'

    photo_url = None if event_status != 'finish' else event_data['photo_url']

    response_data = {
        'date': date,
        'time': time,
        'plan': plan,
        'adress': adress,
        'note': note,
        'event_type': event_type,
        'creator': creator,
        'event_status': event_status,
        'is_expired': is_expired,
        'ready_users': ready_users,
        'maybe_users': maybe_users,
        'no_users': no_users,
        'emoji': emoji,
        'map_link': map_link,
        'user_vote': user_vote,
        'photo_url': photo_url
    }
    del db
    return response_data


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
            'kick': str(user) in str(event_data['blacklist']),
            'id': user
        })

    del db

    return result


@app.route('/api/cancel_event', methods=['POST'])
def cancel_event():
    data = request.get_json()

    event_id = data['event_id']
    reason = data['reason']

    db = Database(db_url)
    event = db.get_data(table='events', filters={'id': event_id})[0]
    event_data = eval(event['data'])

    cancel_text = f'К сожалению, мероприятие отменено. \n\nПричина: {reason}'

    requests.post(f'{db_url}/api/make_mailing', json={'event_id': event_id, 'message': cancel_text})

    event_data['status'] = 'cancel'
    db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')

    del db, bot

    return {'status': 'ok'}


@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.get_json()

    user_id = data['user_id']
    event_id = data['event_id']
    vote = data['vote']

    db = Database(db_url)

    event_data = eval(db.get_data(table='events', filters={'id': event_id})[0]['data'])
    if user_id in event_data['ready']: event_data['ready'].remove(user_id)
    if user_id in event_data['maybe']: event_data['maybe'].remove(user_id)
    if user_id in event_data['no']: event_data['no'].remove(user_id)    
    event_data[vote].append(user_id)
    db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')

    ready_users = [{'name': db.get_data(table='users', filters={'id': user})[0]['name'], 'id': user} for user in event_data['ready']]
    maybe_users = [{'name': db.get_data(table='users', filters={'id': user})[0]['name'], 'id': user} for user in event_data['maybe']]
    no_users = [{'name': db.get_data(table='users', filters={'id': user})[0]['name'], 'id': user} for user in event_data['no']]
    
    return {'status': 'ok', 'ready_users': ready_users, 'maybe_users': maybe_users, 'no_users': no_users}


@app.route('/api/kick_user', methods=['POST'])
def kick_user():
    data = request.get_json()

    user_id = data['user_id']
    event_id = data['event_id']

    db = Database(db_url)

    event = db.get_data(table='events', filters={'id': event_id})[0]
    event_data = eval(event['data'])

    user_name = db.get_data(table='users', filters={'id': user_id})[0]['name']

    status = None
    if str(user_id) in str(event_data['blacklist']):
        event_data['blacklist'].remove(user_id)
        db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')

        del db

        status = 'remove'
    else:
        event_data['blacklist'].append(user_id)
        db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')

        status = 'kick'

    event_type = "Частное" if len(event_data['blacklist']) != 0 else "Открытое"

    return {'status': status, 'name': user_name, 'type': event_type}


@app.route('/api/make_mailing', methods=['POST'])
def make_mailing_api():
    data = request.get_json()

    event_id = data['event_id']
    message = data['message']

    requests.post(f'{db_url}/api/make_mailing', json={'event_id': event_id, 'message': message})

    return {'status': 'ok'}


@app.route('/api/complete', methods=['POST'])
def complete_api():
    data = request.get_json()

    event_id = data['event_id']
    photo_url = data['photo_url'] if data['photo_url'] else None

    db = Database(db_url)
    event = db.get_data(table='events', filters={'id': event_id})[0]
    event_data = eval(event['data'])

    event_data['status'] = 'finish'
    event_data['photo_url'] = photo_url
    db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')

    del db

    return {'status': 'ok'}


@app.route('/api/get_events_list')
def get_events_list():
    db = Database(db_url)

    events: list = db.get_data(table='events', filters={'type': 'event'})
    result = []

    for event in events:
        status = eval(event['data'])['status']
        
        if status == 'new':
            event['human_date'] = utils.beautify_date(event['date'])
            event['cover_url'] = utils.get_file_url(event['photo'])
            event['emoji'] = event['text'].split()[0]
            result.append(event)


    def sort_by_date(event):
        date_str = event['date']
        date = datetime.strptime(date_str, '%d.%m.%Y')
        return date

    result.sort(key=sort_by_date, reverse=False)

    return result